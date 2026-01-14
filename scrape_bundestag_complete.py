import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_all_bundestag_members():
    """
    Scrape all members from the AJAX endpoint which returns Wahlkreis data
    """
    
    # The AJAX endpoint
    ajax_url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/440474-440474"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    print("Fetching members data...")
    response = requests.get(ajax_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    members_dict = {}  # Use dict to avoid duplicates, key is mdbId
    
    # Find all Wahlkreis sections
    wahlkreis_sections = soup.find_all('div', class_='bt-wk-result')
    print(f"Found {len(wahlkreis_sections)} Wahlkreis sections")
    
    for section in wahlkreis_sections:
        # Get Wahlkreis title (e.g., "Wahlkreis 039 Stadt Osnabrück")
        wahlkreis_title_elem = section.find('h3')
        wahlkreis_title = wahlkreis_title_elem.get_text(strip=True) if wahlkreis_title_elem else ""
        
        # Extract Wahlkreis number
        wahlkreis_match = re.search(r'Wahlkreis (\d+)', wahlkreis_title)
        wahlkreis_num = wahlkreis_match.group(1) if wahlkreis_match else None
        
        print(f"\nProcessing: {wahlkreis_title}")
        
        # Find "Orte in diesem Wahlkreis" section to get cities/PLZ
        orte_section = section.find('div', id=re.compile(r'^orte\d+'))
        cities = []
        if orte_section:
            # Extract all cities from this section
            cities_text = orte_section.get_text()
            # Cities are typically in paragraphs or h3 tags
            city_elems = orte_section.find_all(['p', 'h3'])
            for elem in city_elems:
                city = elem.get_text(strip=True)
                if city and not city.startswith('Zu diesem Wahlkreis'):
                    cities.append(city)
        
        # Find all member links in this Wahlkreis
        member_links = section.find_all('a', attrs={'data-id': True})
        
        for link in member_links:
            mdb_id = link.get('data-id')
            
            if not mdb_id:
                continue
            
            # Extract member name from the person element
            person_elem = link.find('div', class_='bt-teaser-person')
            if person_elem:
                name_elem = person_elem.find('h3', class_='bt-person__lastname')
                member_name = name_elem.get_text(strip=True) if name_elem else ""
                
                fraktion_elem = person_elem.find('p', class_='bt-person-fraktion')
                fraktion = fraktion_elem.get_text(strip=True) if fraktion_elem else ""
            else:
                member_name = link.get('title', '')
                fraktion = ""
            
            # Check member type (Wahlkreismandat or Landesliste)
            mandate_type = ""
            parent = link.find_parent('div', class_='col-xs-12')
            if parent:
                h4 = parent.find_previous_sibling('div', class_='col-xs-12')
                if not h4:
                    h4 = parent.find('h4', class_='small')
                if not h4:
                    # Try finding in parent structure
                    col_parent = link.find_parent('div', class_=['col-sm-3', 'col-sm-4', 'col-sm-9'])
                    if col_parent:
                        h4 = col_parent.find_previous_sibling('div')
                        if h4:
                            h4 = h4.find('h4')
                
                if h4 and isinstance(h4, dict):
                    h4 = None
                    
                if h4:
                    h4_text = h4.get_text(strip=True) if hasattr(h4, 'get_text') else ""
                    if 'Wahlkreismandat' in h4_text:
                        mandate_type = "Direktmandat (Wahlkreis)"
                    elif 'Landesliste' in h4_text or 'Über Landesliste' in h4_text:
                        mandate_type = "Listenmandat (Landesliste)"
            
            if mdb_id not in members_dict:
                members_dict[mdb_id] = {
                    'name': member_name,
                    'mdbId': mdb_id,
                    'fraktion': fraktion,
                    'wahlkreis': wahlkreis_title,
                    'wahlkreis_number': wahlkreis_num,
                    'mandate_type': mandate_type,
                    'cities': cities,
                    'profile_url': f"https://www.bundestag.de/abgeordnete/biografien/{member_name.split(',')[0][0].upper()}/{link.get('href', '').split('/')[-1]}" if link.get('href') else "",
                    'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}"
                }
                
                print(f"  - {member_name} ({fraktion}) mdbId={mdb_id}, {mandate_type}")
    
    members_list = list(members_dict.values())
    return members_list


def get_members_with_plz():
    """
    Try to search for individual members and extract PLZ from their pages
    """
    print("\n" + "="*70)
    print("Attempting to get members list with PLZ data...")
    print("="*70)
    
    # Try the alphabetical listing
    alphabet_url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/525250/525262"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    try:
        print(f"Fetching from: {alphabet_url}")
        response = requests.get(alphabet_url, headers=headers)
        
        if response.status_code == 200:
            with open('bundestag_alphabet_list.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("✓ Saved alphabet list response")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find member cards
            members_data = []
            member_elements = soup.find_all('div', class_=re.compile(r'bt-teaser|col-xs'))
            
            # Look for links with data-id
            all_member_links = soup.find_all('a', attrs={'data-id': True})
            print(f"Found {len(all_member_links)} member links")
            
            for link in all_member_links:
                mdb_id = link.get('data-id')
                member_name = link.get('title', '')
                
                # Try to find PLZ or city info nearby
                parent = link.find_parent(['div', 'li', 'article'])
                if parent:
                    text = parent.get_text()
                    # Look for PLZ pattern
                    plz_matches = re.findall(r'\b(\d{5})\b', text)
                    city_match = re.search(r'(\w+),\s*(\d{5})', text)
                    
                    member_info = {
                        'name': member_name,
                        'mdbId': mdb_id,
                        'plz': plz_matches[0] if plz_matches else None,
                        'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}"
                    }
                    members_data.append(member_info)
            
            return members_data
        
    except Exception as e:
        print(f"Error: {e}")
    
    return []


if __name__ == "__main__":
    # Get all members from Wahlkreis data
    members = scrape_all_bundestag_members()
    
    # Also try alphabet listing
    alphabet_members = get_members_with_plz()
    
    # Merge data if we got anything from alphabet listing
    if alphabet_members:
        print(f"\nGot {len(alphabet_members)} members from alphabet listing")
        # Update with PLZ if available
        mdb_dict = {m['mdbId']: m for m in members}
        for alpha_member in alphabet_members:
            mdb_id = alpha_member['mdbId']
            if mdb_id in mdb_dict:
                if alpha_member.get('plz'):
                    mdb_dict[mdb_id]['plz'] = alpha_member['plz']
        members = list(mdb_dict.values())
    
    if members:
        # Save to JSON
        with open('bundestag_members_full.json', 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)
        
        # Save to CSV
        import csv
        with open('bundestag_members_full.csv', 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['name', 'mdbId', 'fraktion', 'wahlkreis', 'wahlkreis_number', 'mandate_type', 'contact_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(members)
        
        # Create simple CSV with just mdbId and wahlkreis_number (as proxy for PLZ region)
        with open('bundestag_members_simple.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'mdbId', 'Wahlkreis_Number', 'Contact_URL'])
            for m in members:
                writer.writerow([m['name'], m['mdbId'], m.get('wahlkreis_number', ''), m['contact_url']])
        
        print(f"\n{'='*70}")
        print(f"✓ SUCCESS: Extracted {len(members)} members")
        print(f"{'='*70}")
        print(f"\nFiles created:")
        print(f"  - bundestag_members_full.json   (Complete data)")
        print(f"  - bundestag_members_full.csv    (CSV format)")
        print(f"  - bundestag_members_simple.csv  (Simple: Name, mdbId, Wahlkreis, URL)")
        
        print(f"\nSample (first 5 members):")
        for member in members[:5]:
            print(f"  {member['name']}")
            print(f"    mdbId: {member['mdbId']}")
            print(f"    Fraktion: {member.get('fraktion', 'N/A')}")
            print(f"    Wahlkreis: {member.get('wahlkreis', 'N/A')}")
            print(f"    Contact: {member['contact_url']}")
            print()
        
        # Summary statistics
        print(f"\nStatistics:")
        print(f"  Total members: {len(members)}")
        fraktionen = {}
        for m in members:
            frak = m.get('fraktion', 'Unknown')
            fraktionen[frak] = fraktionen.get(frak, 0) + 1
        print(f"  By Fraktion:")
        for frak, count in sorted(fraktionen.items(), key=lambda x: -x[1]):
            print(f"    {frak}: {count}")
    else:
        print("\n❌ No members extracted.")
