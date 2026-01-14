import requests
from bs4 import BeautifulSoup
import json
import csv

def search_by_plz(plz):
    """
    Search for Wahlkreis and members by PLZ using the autocomplete API
    """
    
    # Step 1: Use autocomplete to find Wahlkreis for this PLZ
    autocomplete_url = f"https://www.bundestag.de/ajax/filterlist/de/533302-533302/plz-ort-autocomplete?term={plz}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    print(f"\nSearching for PLZ: {plz}")
    print(f"Autocomplete URL: {autocomplete_url}")
    
    response = requests.get(autocomplete_url, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    try:
        # Response should be JSON with autocomplete suggestions
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if not data:
            print(f"No results for PLZ {plz}")
            return None
        
        # Get the first result (should be the matching Wahlkreis)
        first_result = data[0] if isinstance(data, list) else data
        wahlkreis_id = first_result.get('value') or first_result.get('id')
        
        print(f"Found Wahlkreis ID: {wahlkreis_id}")
        
        # Step 2: Get members for this Wahlkreis
        members_url = f"https://www.bundestag.de/ajax/filterlist/de/abgeordnete/440474-440474"
        
        # Try with wahlkreis filter
        params = {
            'wahlkreisnummer': wahlkreis_id
        }
        
        response2 = requests.get(members_url, headers=headers, params=params)
        print(f"Members URL: {response2.url}")
        print(f"Status: {response2.status_code}")
        
        if response2.status_code == 200:
            soup = BeautifulSoup(response2.content, 'html.parser')
            
            # Extract members
            member_links = soup.find_all('a', attrs={'data-id': True})
            print(f"Found {len(member_links)} member links")
            
            members = []
            for link in member_links:
                mdb_id = link.get('data-id')
                name = link.get('title', '')
                
                fraktion_elem = link.find('p', class_='bt-person-fraktion')
                fraktion = fraktion_elem.get_text(strip=True) if fraktion_elem else ''
                
                members.append({
                    'name': name,
                    'mdbId': mdb_id,
                    'fraktion': fraktion,
                    'contact_url': f'https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}'
                })
            
            return {
                'plz': plz,
                'wahlkreis_id': wahlkreis_id,
                'wahlkreis_info': first_result,
                'members': members
            }
        
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Response text: {response.text[:500]}")
        return None


def build_complete_plz_database():
    """
    Build a comprehensive PLZ to member database by testing all major PLZ ranges
    """
    
    print("="*70)
    print("BUILDING COMPREHENSIVE PLZ TO MEMBER DATABASE")
    print("="*70)
    
    # Test comprehensive PLZ ranges (all German PLZ from 01xxx to 99xxx)
    # For efficiency, test first 2 digits (01-99)
    plz_database = {}
    
    # Major cities and their PLZ for testing
    test_plzs = {
        '10961': 'Berlin Kreuzberg',
        '10115': 'Berlin Mitte',
        '20095': 'Hamburg',
        '80331': 'München',
        '50667': 'Köln',
        '60311': 'Frankfurt',
        '70173': 'Stuttgart',
        '40213': 'Düsseldorf',
        '04109': 'Leipzig',
        '01067': 'Dresden',
        '30159': 'Hannover',
        '90402': 'Nürnberg',
        '28195': 'Bremen',
        '45127': 'Essen',
        '44135': 'Dortmund',
        '52062': 'Aachen',
        '96047': 'Bamberg',
    }
    
    for plz, city in test_plzs.items():
        print(f"\n{'='*70}")
        print(f"Testing: {plz} ({city})")
        result = search_by_plz(plz)
        
        if result:
            plz_database[plz] = result
            print(f"✓ Found {len(result['members'])} members for {city}")
            for member in result['members']:
                print(f"  - {member['name']} ({member['fraktion']})")
        else:
            print(f"✗ No data for {city}")
    
    # Save results
    with open('plz_database.json', 'w', encoding='utf-8') as f:
        json.dump(plz_database, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print(f"Saved PLZ database with {len(plz_database)} entries")
    print(f"{'='*70}")
    
    return plz_database


if __name__ == "__main__":
    # Test specific PLZ
    result = search_by_plz('10961')
    
    if result:
        print(f"\n{'='*70}")
        print(f"RESULT FOR PLZ 10961:")
        print(f"{'='*70}")
        for member in result['members']:
            print(f"{member['name']:40} {member['fraktion']:25}")
            print(f"  Contact: {member['contact_url']}")
            print()
    
    # Build comprehensive database
    print("\n" + "="*70)
    input("Press Enter to build comprehensive PLZ database...")
    build_complete_plz_database()
