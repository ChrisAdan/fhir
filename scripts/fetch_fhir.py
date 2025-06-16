import requests, json, time
from pathlib import Path

BASE_URL = 'https://hapi.fhir.org/baseR4'
RESOURCES = {
    'Condition': 'subject',
    'Observation': 'subject',
    'Encounter': 'subject',
    'MedicationRequest': 'subject',
    'Procedure': 'subject',
    'AllergyIntolerance': 'patient',
    'Device': 'patient',
    'Immunization': 'patient'
}
BATCH_SIZE = 1000
RECORD_LIMIT = 10000
RAWDIR = Path('data/raw_json')
    
def fetch_fhir_resource(resource, base_url=BASE_URL, count=100):
    '''Generator yielding FHIR resources one-by-one, paginated.
    
    Args:
        resource (string): Type of resource to fetch.
        base_url (string): API base URL.
        count (integer, optional): Number of records to fetch. Defaults to 100
    
    Yields:
        (JSON): Iterable list of records
    '''
    url = f'{base_url}/{resource}?_count={count}'
    while url:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        yield from (entry['resource'] for entry in data.get('entry', []))
        url = next((link['url'] for link in data.get('link', []) if link['relation'] == 'next'), None)
        time.sleep(0.1)

def fetch_resource_for_patient(resource, param, patient_id, max_retries=3):
    '''Fetch linked resources for a given patient.
    Args:
        resource (string): Type of resource to fetch.
        param (string): URL parameter to specify 'subject' or 'patient' depending on requirements of resource.
        patient_id (string): Patient ID to search.
        max_retries (int): Number of retries to allow.
    Returns:
        (list): List of Patient IDs retrieved.'''
    url = f'{BASE_URL}/{resource}?{param}=Patient/{patient_id}'
    retries = 0
    while retries < max_retries:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 429:
                wait = int(resp.headers.get('Retry-After', 5))
                print(f'Rate Limited. Waiting {wait} seconds.')
                time.sleep(wait)
                retries += 1
                continue
            resp.raise_for_status()

            data = resp.json()
            if 'entry' not in data:
                return []
            entries = data.get('entry', [])
            return [entry['resource'] for entry in entries if 'resource' in entry]
        except requests.exceptions.RequestException as e:
            print(f'Error fetching {resource} for {patient_id}: {e}')
            retries += 1
            time.sleep(2)
    return []

def extract_existing_patient_ids():
    '''Read patient records from disk and return a set of Patient IDs.
    Returns
        (set): Set of Patient IDs that exist in data/raw_json/patient.'''
    patient_dir = RAWDIR / 'patient'
    if not patient_dir.exists():
        return set()
    
    ids = set()
    for file in patient_dir.glob('*.json'):
        with open(file) as f:
            data = json.load(f)
            for patient in data:
                if isinstance(patient, dict) and 'id' in patient:
                    ids.add(patient['id'])
    return ids

def extract_patient_ids_from_resource(resource):
    '''Get a set of patient IDs already fetched for a given resource.
    Args:
        resource (string): The name of the resource to extract existing Patient IDs.
        
    Returns:
        (set): Set of Patient IDs that exist for the resource.'''
    resource_dir = RAWDIR / resource.lower()
    if not resource_dir.exists():
        return set()

    ids = set()
    for file in resource_dir.glob('*.json'):
        try:
            with open(file) as f:
                data = json.load(f)
                for entry in data:
                    if not isinstance(entry, dict):
                        continue
                    ref = None
                    if 'subject' in entry and isinstance(entry['subject'], dict):
                        ref = entry['subject'].get('reference', '')
                    elif 'patient' in entry and isinstance(entry['patient'], dict):
                        ref = entry['patient'].get('reference', '')
                    if ref and ref.startswith('Patient/'):
                        ids.add(ref.split('/')[-1])
        except Exception as e:
            print(f'Error parsing {file}: {e}')
    return ids

def write_batch_to_disk(resource, batch, batch_num):
    '''Write a batch of resources to a JSON file.
    
    Args:
        resource (string): Type of resource to write.
        batch (list): List of records in batch to write.
        batch_num (integer): Current iteration, written into output filename.'''
    resource_dir = RAWDIR / resource.lower()
    resource_dir.mkdir(parents=True, exist_ok=True)
    filename = resource_dir / f'{resource.lower()}_batch_{batch_num}.json'
    with open(filename, 'w') as file:
        json.dump(batch, file, indent=2)
    print(f'Wrote {len(batch)} {resource} records to {filename}')

def load_skipped_patient_ids(resource):
    """Extract a set of existing Patient IDs that have been searched for and no records exist for given resource.
    Args:
        resource (string): The resource type to search"""
    path = RAWDIR / resource.lower() / 'no_data.json'
    if path.exists():
        with open(path) as f:
            return set(json.load(f))
    return set()

def save_skipped_patient_ids(resource, ids_to_add):
    """Write a set of new Patient IDs to add that have been queried and no records exist for given resource, to avoid requerying.
    Args:
        resource (string): The resource type for skipped IDs to save.
        ids_to_add (set): Set of Patient IDs with no existing records for the resource."""
    path = RAWDIR / resource.lower() / 'no_data.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_skipped_patient_ids(resource)
    combined = existing.union(ids_to_add)
    with open(path, 'w') as f:
        json.dump(list(combined), f, indent=2)

def main():
    # Populate or extract Patient IDs
    patient_dir = RAWDIR / 'patient'
    patient_ids = set()

    if not patient_dir.exists() or not any(patient_dir.glob('*.json')):
        print('No existing patient data - fetching 10K Patients ..')
        patient_dir.mkdir(parents=True, exist_ok=True)
        total = 0
        batch = []
        batch_num = 1

        for patient in fetch_fhir_resource('Patient'):
            batch.append(patient)
            total+= 1
            if len(batch) >= BATCH_SIZE:
                write_batch_to_disk('Patient', batch, batch_num)
                batch = []
                batch_num += 1
            if total >= RECORD_LIMIT:
                break
        if batch:
            write_batch_to_disk('Patient', batch, batch_num)
        print(f'Finished fetching {total} Patients.')
    else:
        print('Found existing Patient records - skipping fetch.')

    patient_ids = extract_existing_patient_ids()
    print(f'Extracted {len(patient_ids)} patient IDs for use.')

    # Fetch resources by patient
    for resource, param in RESOURCES.items():
        print(f'Checking existing records for {resource}.')
        fetched_ids = extract_patient_ids_from_resource(resource)
        skipped_ids = load_skipped_patient_ids(resource)
        missing_ids = patient_ids - fetched_ids - skipped_ids
        print(f'{resource}: {len(fetched_ids)} already fetched. {len(missing_ids)} missing.')

        if not missing_ids:
            print(f'Skipping {resource} - all patient records exist.')
            continue

        print(f'Fetching {resource} for patients ..')
        batch = []
        no_data_patients = set()
        resource_dir = RAWDIR / resource.lower()
        resource_dir.mkdir(parents=True, exist_ok=True)
        batch_num = len(list(resource_dir.glob('*.json'))) + 1

        for i, pid in enumerate(missing_ids):
            results = fetch_resource_for_patient(resource, param, pid)
            if not results:
                print(f'No {resource} returned for patient {pid}')
                no_data_patients.add(pid)
            batch.extend(results)

            if len(batch) >= BATCH_SIZE:
                write_batch_to_disk(resource, batch, batch_num)
                batch = []
                batch_num += 1

            if i % 100 == 0:
                print(f'Processed {i} patients.')
            
        if batch:
            write_batch_to_disk(resource, batch, batch_num)

        if no_data_patients:
            save_skipped_patient_ids(resource, no_data_patients)
            print(f'Saved {len(no_data_patients)} patient IDs that returned no {resource}.')
        print(f'Completed {resource}.')

if __name__ == '__main__':
    main()