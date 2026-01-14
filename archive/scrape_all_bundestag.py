import requests
from bs4 import BeautifulSoup
import json
import re
import time

def get_all_members_complete():
    """
    Get all Bundestag members by trying to fetch the complete filterlist
    """
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    # Try different endpoints to get all members
    endpoints = [
        # Try getting all with limit parameter
        "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/440474-440474?limit=1000",
        # Try alphabetical listing
        "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/525250/525262",
        # Try biography listing
        "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/biografien",
    ]
    
    all_members = {}  # Use dict with mdbId as key to avoid duplicates
    
    for endpoint in endpoints:
        print(f"\nTrying endpoint: {endpoint}")
        try:
            response = requests.get(endpoint, headers=headers, timeout=15)
            if response.status_code == 200:
                print(f"✓ Status 200, content length: {len(response.text)}")
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Method 1: Find all member links with data-id
                member_links = soup.find_all('a', attrs={'data-id': True})
                print(f"  Found {len(member_links)} member links")
                
                for link in member_links:
                    mdb_id = link.get('data-id')
                    if not mdb_id or mdb_id in all_members:
                        continue
                    
                    # Extract member details
                    member_name = link.get('title', '')
                    
                    # Find fraktion
                    fraktion = ""
                    fraktion_elem = link.find('p', class_='bt-person-fraktion')
                    if fraktion_elem:
                        fraktion = fraktion_elem.get_text(strip=True)
                    
                    # Find wahlkreis
                    wahlkreis = ""
                    wahlkreis_num = ""
                    section = link.find_parent('div', class_='bt-wk-result')
                    if section:
                        h3 = section.find('h3')
                        if h3:
                            wahlkreis = h3.get_text(strip=True)
                            wk_match = re.search(r'Wahlkreis (\d+)', wahlkreis)
                            if wk_match:
                                wahlkreis_num = wk_match.group(1)
                    
                    all_members[mdb_id] = {
                        'name': member_name,
                        'mdbId': mdb_id,
                        'fraktion': fraktion,
                        'wahlkreis': wahlkreis,
                        'wahlkreis_number': wahlkreis_num,
                        'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}"
                    }
                
                # Method 2: Look for table rows or list items
                rows = soup.find_all(['tr', 'li'], class_=re.compile(r'member|mdb', re.I))
                if rows:
                    print(f"  Found {len(rows)} potential member rows")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    return list(all_members.values())


def scrape_members_by_letter():
    """
    Scrape members alphabetically (A-Z)
    """
    
    base_url = "https://www.bundestag.de/abgeordnete/biografien"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    all_members = {}
    
    # Letters of German alphabet
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    print("\n" + "="*70)
    print("Scraping members alphabetically...")
    print("="*70)
    
    for letter in letters:
        url = f"{base_url}/{letter.lower()}"
        print(f"\nFetching letter {letter}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for member links
                member_links = soup.find_all('a', href=re.compile(r'/abgeordnete/biografien/.*-\d+'))
                
                for link in member_links:
                    href = link.get('href', '')
                    # Extract mdbId from URL (last number in URL)
                    mdb_match = re.search(r'-(\d+)$', href)
                    if mdb_match:
                        mdb_id = mdb_match.group(1)
                        
                        if mdb_id not in all_members:
                            member_name = link.get_text(strip=True)
                            if not member_name:
                                member_name = link.get('title', '')
                            
                            all_members[mdb_id] = {
                                'name': member_name,
                                'mdbId': mdb_id,
                                'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}",
                                'profile_url': f"https://www.bundestag.de{href}"
                            }
                            print(f"  Found: {member_name} (mdbId: {mdb_id})")
                
                print(f"  Total for {letter}: {len([m for m in all_members.values() if m['name'].startswith(letter)])}")
                
                # Be respectful, add small delay
                time.sleep(0.5)
            else:
                print(f"  Status {response.status_code}")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    return list(all_members.values())


if __name__ == "__main__":
    print("="*70)
    print("BUNDESTAG MEMBER SCRAPER")
    print("="*70)
    
    # Try comprehensive scrape from different endpoints
    members_from_filter = get_all_members_complete()
    print(f"\n✓ Got {len(members_from_filter)} members from filter endpoints")
    
    # Try alphabetical scraping
    members_from_alphabet = scrape_members_by_letter()
    print(f"\n✓ Got {len(members_from_alphabet)} members from alphabetical listing")
    
    # Merge data
    all_members_dict = {}
    
    # Add filter data first (has more detail)
    for member in members_from_filter:
        all_members_dict[member['mdbId']] = member
    
    # Add alphabet data (fill in missing)
    for member in members_from_alphabet:
        mdb_id = member['mdbId']
        if mdb_id not in all_members_dict:
            all_members_dict[mdb_id] = member
        else:
            # Merge data - prefer existing but add missing fields
            if not all_members_dict[mdb_id].get('name'):
                all_members_dict[mdb_id]['name'] = member['name']
            if not all_members_dict[mdb_id].get('profile_url'):
                all_members_dict[mdb_id]['profile_url'] = member.get('profile_url', '')
    
    final_members = list(all_members_dict.values())
    
    # Sort by name
    final_members.sort(key=lambda x: x.get('name', ''))
    
    if final_members:
        print(f"\n{'='*70}")
        print(f"✓✓✓ FINAL RESULT: {len(final_members)} unique members extracted ✓✓✓")
        print(f"{'='*70}")
        
        # Save to JSON
        with open('bundestag_all_members.json', 'w', encoding='utf-8') as f:
            json.dump(final_members, f, ensure_ascii=False, indent=2)
        
        # Save to CSV
        import csv
        with open('bundestag_all_members.csv', 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['name', 'mdbId', 'fraktion', 'wahlkreis_number', 'contact_url', 'profile_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(final_members)
        
        # Create simple CSV for easy use
        with open('bundestag_mdbid_list.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'mdbId', 'Wahlkreis_Number', 'Contact_URL'])
            for m in final_members:
                writer.writerow([
                    m.get('name', ''),
                    m['mdbId'],
                    m.get('wahlkreis_number', ''),
                    m['contact_url']
                ])
        
        print(f"\n📄 Files created:")
        print(f"  1. bundestag_all_members.json    - Complete JSON data")
        print(f"  2. bundestag_all_members.csv     - CSV with all fields")
        print(f"  3. bundestag_mdbid_list.csv      - Simple list (Name, mdbId, Wahlkreis, URL)")
        
        print(f"\n📊 Sample data (first 10 members):")
        for i, member in enumerate(final_members[:10], 1):
            print(f"{i:2}. {member.get('name', 'N/A')}")
            print(f"     mdbId: {member['mdbId']}")
            print(f"     Contact: {member['contact_url']}")
            if member.get('fraktion'):
                print(f"     Fraktion: {member['fraktion']}")
            if member.get('wahlkreis_number'):
                print(f"     Wahlkreis: {member['wahlkreis_number']}")
        
        # Statistics
        print(f"\n📈 Statistics:")
        print(f"  Total members: {len(final_members)}")
        
        with_fraktion = len([m for m in final_members if m.get('fraktion')])
        with_wahlkreis = len([m for m in final_members if m.get('wahlkreis_number')])
        
        print(f"  Members with Fraktion info: {with_fraktion}")
        print(f"  Members with Wahlkreis info: {with_wahlkreis}")
        
        if with_fraktion > 0:
            fraktionen = {}
            for m in final_members:
                frak = m.get('fraktion', '').strip()
                if frak:
                    fraktionen[frak] = fraktionen.get(frak, 0) + 1
            
            print(f"\n  By Fraktion:")
            for frak, count in sorted(fraktionen.items(), key=lambda x: -x[1]):
                print(f"    {frak}: {count}")
    else:
        print("\n❌ No members extracted")
