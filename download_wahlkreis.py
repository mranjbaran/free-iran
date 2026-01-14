import requests
import json
import csv

def download_wahlkreis_data():
    """
    Download and process the Wahlkreis JSON data
    """
    
    url = "https://www.bundestag.de/static/appdata/includes/datasources/wahlkreisergebnisse/btwahl2025/wahlkreise.json"
    
    print(f"Downloading from {url}...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    data = response.json()
    print(f"Found {len(data)} entries")
    
    # Save raw data
    with open('wahlkreise_raw.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Saved to wahlkreise_raw.json")
    
    # Examine structure
    print("\nData structure:")
    if data:
        first_item = data[0]
        print(json.dumps(first_item, indent=2, ensure_ascii=False))
    
    return data


def create_comprehensive_plz_database():
    """
    Create comprehensive PLZ to member database
    We need to map Wahlkreis winners to our member list
    """
    
    print("\n" + "="*70)
    print("Creating comprehensive PLZ database...")
    print("="*70)
    
    # Load member data
    print("\n1. Loading member data...")
    members = {}
    members_by_name = {}
    
    with open('bundestag_complete.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mdb_id = row['mdbId']
            members[mdb_id] = row
            
            # Also index by name for matching
            name = row['name']
            members_by_name[name] = row
    
    print(f"   Loaded {len(members)} members")
    
    # Load Wahlkreis data
    print("\n2. Loading Wahlkreis data...")
    wahlkreise = download_wahlkreis_data()
    
    if not wahlkreise:
        return None
    
    # Build PLZ mapping
    print("\n3. Building PLZ mapping...")
    plz_database = {}
    
    for wk in wahlkreise:
        print(f"\nProcessing: {wk.get('wahlkreis_name', 'Unknown')}")
        print(f"  Keys: {list(wk.keys())}")
        
    # The data structure is different than expected
    # Let's see what we actually have
    print("\n" + "="*70)
    print("FULL DATA EXAMINATION:")
    print("="*70)
    for i, wk in enumerate(wahlkreise):
        print(f"\n--- Entry {i+1} ---")
        for key, value in wk.items():
            if isinstance(value, (list, dict)):
                print(f"{key}: {type(value).__name__} with {len(value)} items")
            else:
                print(f"{key}: {value}")
    
    return wahlkreise


if __name__ == "__main__":
    data = create_comprehensive_plz_database()
