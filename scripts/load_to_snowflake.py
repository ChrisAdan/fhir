import json
import os
from pathlib import Path
from datetime import datetime
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
from shutil import move

RAW_DIR = Path('data/raw_json')
PROCESSED_DIR = Path('data/processed_json')
SCHEMA = os.environ['SNOWFLAKE_SCHEMA']
DATABASE = os.environ['SNOWFLAKE_DATABASE']

def get_snowflake_connection():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend

    rsa_pem_path = os.environ['RSA_PEM']

    with open(rsa_pem_path, 'rb') as key_file:
        p_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    private_key = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return snowflake.connector.connect(
        user=os.environ['SNOWFLAKE_USER'],
        account=os.environ['SNOWFLAKE_ACCOUNT'],
        private_key=private_key,
        warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
        database=DATABASE,
        schema=SCHEMA,
        role=os.environ['SNOWFLAKE_ROLE']
    )

def init_snowflake_session(conn):
    with conn.cursor() as cur:
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {DATABASE}.{SCHEMA}")
        cur.execute(f"USE DATABASE {DATABASE}")
        cur.execute(f"USE SCHEMA {SCHEMA}")

def drop_raw_table(conn, table_name):
    qualified_table_name = f'{DATABASE}.{SCHEMA}.{table_name}'
    drop_sql = f'''
    drop table if exists {qualified_table_name};
    '''
    with conn.cursor() as cur:
        cur.execute(f'USE ROLE {os.environ["SNOWFLAKE_ROLE"]};')
        cur.execute(drop_sql)

def ensure_table_exists(conn, table_name):
    qualified_table_name = f'{DATABASE}.{SCHEMA}.{table_name}'
    create_sql = f'''
    create table if not exists {qualified_table_name}(
        ID string primary key,
        RAW_RESPONSE variant,
        CREATED_AT timestamp_ltz default current_timestamp,
        FILE_ID string
    );
    '''
    with conn.cursor() as cur:
        cur.execute(create_sql)

def load_json_file_to_df(filepath):
    with open(filepath) as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f'Expected list in {filepath}, got {type(data)}')
    records = []
    for entry in data:
        record_id = entry.get('id')
        if not record_id:
            continue
        records.append({
            'ID':record_id,
            'RAW_RESPONSE':entry,
            'FILE_ID':filepath.name
        })
    return pd.DataFrame(records)

def load_resource_batches(conn, resource, dev):
    folder = RAW_DIR / resource.lower()
    if not folder.exists():
        print(f'Skipping {resource} - folder not found.')
        return

    table_name = f'RAW_{resource.upper()}'
    if dev:
        drop_raw_table(conn, table_name)
    ensure_table_exists(conn, table_name)

    existing_file_names = set()
    try:
        with conn.cursor() as cur:
            cur.execute(f'select distinct file_id from {table_name}')
            existing_file_names = {row[0] for row in cur.fetchall()}
            print(f'{resource}: Found {len(existing_file_names)} files already loaded in {table_name}')
    except Exception as e:
        print(f'Error querying existing file names from {table_name}: {e}')
        return
    batch_files = sorted(f for f in folder.glob('*.json') if f.name != 'no_data.json')
    print(f'{resource}: Found {len(batch_files)} batch files.')

    for i, filepath in enumerate(batch_files, 1):
        file_id = filepath.name
        # Don't want to load files twice
        if file_id in existing_file_names:
            print(f'Skipping already loaded file: {file_id}')
            archive_file(filepath, resource)
            continue

        try:
            df = load_json_file_to_df(filepath)
            if df.empty:
                print(f'Skipping empty batch file: {filepath.name}')
                archive_file(filepath, resource)
                continue
            try:
                success, nchunks, nrows, _ = write_pandas(conn, df, table_name, quote_identifiers=False)
                print(f"[{resource}] Batch {i}/{len(batch_files)}: {nrows} rows inserted into {table_name}")
                archive_file(filepath, resource)
            except Exception as e:
                print(f'Error writing {filepath.name} to {table_name}')
                continue
        except Exception as e:
            print(f'Error loading {filepath.name}: {e}')

def archive_file(filepath: Path, resource: str):
    dest_dir = PROCESSED_DIR / resource.lower()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / filepath.name
    move(str(filepath), str(dest))

def main():
    dev = False
    conn = get_snowflake_connection()
    init_snowflake_session(conn)
    if dev:
        with conn.cursor() as cur:
            cur.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE(), CURRENT_SCHEMA();")
            result = cur.fetchone()
            print(f"User: {result[0]}, Role: {result[1]}, Database: {result[2]}, Schema: {result[3]}")
    resources = [f.name for f in RAW_DIR.iterdir() if f.is_dir()]
    for resource in resources:
        load_resource_batches(conn, resource, dev)
    conn.close()

if __name__ == '__main__':
    main()