import requests
from bs4 import BeautifulSoup
import json
import re

def test_endpoints():
    """Test which endpoints actually work"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    endpoints = [
        "https://www.bundestag.de/abgeordnete",
        "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/440474-440474",
        "https://www.bundestag.de/abgeordnete/biografien",
    ]
    
    print("Testing endpoints...")
    for url in endpoints:
        try:
            print(f"\n{url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Content length: {len(response.text)}")
            
            if response.status_code == 200:
                # Check for mdbId
                mdb_count = len(re.findall(r'data-id="\d+"', response.text))
                print(f"  Contains data-id attributes: {mdb_count}")
                
                # Check for biographical links
                bio_count = len(re.findall(r'/abgeordnete/biografien/[A-Z]/\w+-\d+', response.text))
                print(f"  Contains biography links: {bio_count}")
                
        except Exception as e:
            print(f"  Error: {e}")


def scrape_members_from_main_page():
    """
    Scrape from the main biographies page
    """
    
    url = "https://www.bundestag.de/abgeordnete/biografien"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    print("\n" + "="*70)
    print("Scraping from biografien page...")
    print("="*70)
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Error: Status {response.status_code}")
            return []
        
        # Save for inspection
        with open('biografien_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Saved page to biografien_page.html")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        members = []
        
        # Find all biography links
        bio_links = soup.find_all('a', href=re.compile(r'/abgeordnete/biografien/[A-Z]/[\w-]+-(\d+)'))
        print(f"Found {len(bio_links)} biography links")
        
        for link in bio_links:
            href = link.get('href', '')
            # Extract mdbId from URL
            mdb_match = re.search(r'-(\d+)$', href)
            if mdb_match:
                mdb_id = mdb_match.group(1)
                
                # Get name
                name = link.get_text(strip=True)
                if not name:
                    name = link.get('title', '')
                
                # Look for additional info in parent
                parent = link.find_parent(['div', 'li', 'article', 'tr'])
                fraktion = ""
                wahlkreis = ""
                
                if parent:
                    # Look for fraktion/party info
                    text = parent.get_text()
                    for party in ['CDU/CSU', 'SPD', 'Bündnis 90/Die Grünen', 'Die Grünen', 'FDP', 'AfD', 'Die Linke', 'BSW']:
                        if party in text:
                            fraktion = party
                            break
                
                member = {
                    'name': name,
                    'mdbId': mdb_id,
                    'fraktion': fraktion,
                    'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}",
                    'profile_url': f"https://www.bundestag.de{href}"
                }
                
                members.append(member)
                print(f"  {name} - mdbId: {mdb_id}")
        
        return members
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []


def scrape_ajax_endpoint():
    """
    Scrape the AJAX endpoint that we know works
    """
    
    url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/440474-440474"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html',
        'Referer': 'https://www.bundestag.de/abgeordnete',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    print("\n" + "="*70)
    print("Scraping AJAX endpoint...")
    print("="*70)
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"Error: Status {response.status_code}")
            return []
        
        print(f"Response length: {len(response.text)} chars")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        members = []
        seen_ids = set()
        
        # Find all member links with data-id
        member_links = soup.find_all('a', attrs={'data-id': True})
        print(f"Found {len(member_links)} members with data-id")
        
        for link in member_links:
            mdb_id = link.get('data-id')
            
            if mdb_id in seen_ids:
                continue
            seen_ids.add(mdb_id)
            
            # Get name
            name = link.get('title', '')
            
            # Get fraktion
            fraktion = ""
            fraktion_elem = link.find('p', class_='bt-person-fraktion')
            if fraktion_elem:
                fraktion = fraktion_elem.get_text(strip=True)
            
            # Get Wahlkreis
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
            
            member = {
                'name': name,
                'mdbId': mdb_id,
                'fraktion': fraktion,
                'wahlkreis': wahlkreis,
                'wahlkreis_number': wahlkreis_num,
                'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}"
            }
            
            members.append(member)
        
        print(f"Extracted {len(members)} unique members")
        return members
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    # Test endpoints first
    test_endpoints()
    
    # Try biografien page
    members_bio = scrape_members_from_main_page()
    
    # Try AJAX endpoint
    members_ajax = scrape_ajax_endpoint()
    
    # Merge results
    all_members = {}
    
    for member in members_bio + members_ajax:
        mdb_id = member['mdbId']
        if mdb_id not in all_members:
            all_members[mdb_id] = member
        else:
            # Merge data - update with non-empty values
            for key, value in member.items():
                if value and not all_members[mdb_id].get(key):
                    all_members[mdb_id][key] = value
    
    final_members = list(all_members.values())
    final_members.sort(key=lambda x: x.get('name', ''))
    
    if final_members:
        print(f"\n{'='*70}")
        print(f"SUCCESS: {len(final_members)} members extracted")
        print(f"{'='*70}")
        
        # Save to files
        import csv
        
        # JSON
        with open('bundestag_members.json', 'w', encoding='utf-8') as f:
            json.dump(final_members, f, ensure_ascii=False, indent=2)
        
        # CSV
        with open('bundestag_members.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'mdbId', 'fraktion', 'wahlkreis_number', 'contact_url'], extrasaction='ignore')
            writer.writeheader()
            writer.writerows(final_members)
        
        # Simple list
        with open('mdbid_list.txt', 'w', encoding='utf-8') as f:
            for m in final_members:
                f.write(f"{m['mdbId']},{m.get('name', 'N/A')},{m.get('wahlkreis_number', 'N/A')}\n")
        
        print(f"\nFiles created:")
        print(f"  - bundestag_members.json")
        print(f"  - bundestag_members.csv")
        print(f"  - mdbid_list.txt")
        
        print(f"\nFirst 10 members:")
        for i, m in enumerate(final_members[:10], 1):
            print(f"{i}. {m['name']} (mdbId: {m['mdbId']})")
            print(f"   URL: {m['contact_url']}")
    else:
        print("\nNo members extracted. Check error messages above.")
