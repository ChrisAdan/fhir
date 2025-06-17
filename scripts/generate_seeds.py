from pathlib import Path
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

script_dir = Path(__file__).resolve().parent
dbt_project_path = (script_dir / '../dbt_project.yml').resolve()

data_dir = dbt_project_path.parent / 'seeds' / 'loinc'

project_name = 'ecart'
dim_schema = 'dim'

with dbt_project_path.open('r') as f:
    dbt_config = yaml.load(f)

seeds = dbt_config.setdefault('seeds', {})
project_seeds = seeds.setdefault(project_name, {})

csv_files = sorted(data_dir.glob('dim_loinc_*.csv'))

added_count = 0
for csv_file in csv_files:
    seed_name = csv_file.stem
    if seed_name not in project_seeds:
        project_seeds[seed_name] = {
            'file': csv_file.name,
            '+schema': 'dim'}
        added_count += 1

with dbt_project_path.open('w') as f:
    yaml.dump(dbt_config, f)

print(f'Added {added_count} new seed(s) to {dbt_project_path}')