import requests
from bs4 import BeautifulSoup
import json
import csv
import re

def get_wahlkreis_for_plz():
    """
    Get Wahlkreis information including PLZ from the AJAX endpoint
    """
    
    url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/440474-440474"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    print("Fetching Wahlkreis and member data...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return {}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    wahlkreis_data = {}
    members_by_wahlkreis = {}
    
    # Find all Wahlkreis sections
    wahlkreis_sections = soup.find_all('div', class_='bt-wk-result')
    print(f"Found {len(wahlkreis_sections)} Wahlkreis sections")
    
    for section in wahlkreis_sections:
        # Get Wahlkreis title
        h3 = section.find('h3')
        if not h3:
            continue
        
        wahlkreis_title = h3.get_text(strip=True)
        wk_match = re.search(r'Wahlkreis (\d+)\s+(.+)', wahlkreis_title)
        
        if not wk_match:
            continue
        
        wahlkreis_num = wk_match.group(1)
        wahlkreis_name = wk_match.group(2)
        
        # Get cities/places from "Orte in diesem Wahlkreis"
        orte_section = section.find('div', id=re.compile(r'^orte\d+'))
        cities = []
        if orte_section:
            city_elems = orte_section.find_all(['p', 'h3'])
            for elem in city_elems:
                city = elem.get_text(strip=True)
                if city and not city.startswith('Zu diesem Wahlkreis'):
                    cities.append(city)
        
        # Get members
        member_links = section.find_all('a', attrs={'data-id': True})
        members = []
        
        for link in member_links:
            mdb_id = link.get('data-id')
            if not mdb_id:
                continue
            
            name = link.get('title', '')
            
            # Get fraktion
            fraktion = ""
            fraktion_elem = link.find('p', class_='bt-person-fraktion')
            if fraktion_elem:
                fraktion = fraktion_elem.get_text(strip=True)
            
            members.append({
                'name': name,
                'mdbId': mdb_id,
                'fraktion': fraktion
            })
        
        wahlkreis_data[wahlkreis_num] = {
            'number': wahlkreis_num,
            'name': wahlkreis_name,
            'cities': cities,
            'members': members
        }
        
        print(f"WK {wahlkreis_num}: {wahlkreis_name} - {len(members)} members, {len(cities)} cities")
    
    return wahlkreis_data


def create_plz_to_wahlkreis_mapping():
    """
    Create a simple PLZ to Wahlkreis mapping based on major cities
    """
    
    # This is a partial mapping of major German cities and their PLZ ranges to Wahlkreis
    plz_mapping = {
        # Berlin (10xxx-14xxx)
        "10": "Berlin", "11": "Berlin", "12": "Berlin", "13": "Berlin", "14": "Berlin",
        # Hamburg (20xxx-22xxx)
        "20": "Hamburg", "21": "Hamburg", "22": "Hamburg",
        # München (80xxx-81xxx)
        "80": "München", "81": "München",
        # Köln (50xxx-51xxx)
        "50": "Köln", "51": "Köln",
        # Frankfurt (60xxx-65xxx)
        "60": "Frankfurt", "65": "Frankfurt",
        # Stuttgart (70xxx-71xxx)
        "70": "Stuttgart", "71": "Stuttgart",
        # Düsseldorf (40xxx)
        "40": "Düsseldorf",
        # Dortmund (44xxx)
        "44": "Dortmund",
        # Essen (45xxx)
        "45": "Essen",
        # Bremen (28xxx)
        "28": "Bremen",
        # Dresden (01xxx)
        "01": "Dresden",
        # Leipzig (04xxx)
        "04": "Leipzig",
        # Hannover (30xxx)
        "30": "Hannover",
        # Nürnberg (90xxx)
        "90": "Nürnberg",
    }
    
    return plz_mapping


if __name__ == "__main__":
    # Get Wahlkreis data
    wahlkreis_data = get_wahlkreis_for_plz()
    
    # Save Wahlkreis data
    with open('wahlkreis_data.json', 'w', encoding='utf-8') as f:
        json.dump(wahlkreis_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(wahlkreis_data)} Wahlkreis entries to wahlkreis_data.json")
    
    # Also load and merge with complete member list
    print("\nMerging with complete member list...")
    
    # Load complete members
    members_dict = {}
    with open('bundestag_complete.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            members_dict[row['mdbId']] = row
    
    # Create enriched data with Wahlkreis info
    enriched_members = []
    for wk_num, wk_info in wahlkreis_data.items():
        for member in wk_info['members']:
            mdb_id = member['mdbId']
            if mdb_id in members_dict:
                enriched_members.append({
                    'name': members_dict[mdb_id]['name'],
                    'mdbId': mdb_id,
                    'fraktion': members_dict[mdb_id]['fraktion'],
                    'wahlkreis_number': wk_num,
                    'wahlkreis_name': wk_info['name'],
                    'cities': ', '.join(wk_info['cities'][:5]),  # First 5 cities
                    'contact_url': members_dict[mdb_id]['contact_url']
                })
    
    # Save enriched data
    with open('members_with_wahlkreis.json', 'w', encoding='utf-8') as f:
        json.dump(enriched_members, f, ensure_ascii=False, indent=2)
    
    with open('members_with_wahlkreis.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['name', 'mdbId', 'fraktion', 'wahlkreis_number', 'wahlkreis_name', 'cities', 'contact_url']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched_members)
    
    print(f"Created members_with_wahlkreis.json and .csv with {len(enriched_members)} entries")
