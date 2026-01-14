import requests
from bs4 import BeautifulSoup
import json
import re
import time

def scrape_bundestag_members_ajax():
    """
    Scrape mdbId and PLZ from Bundestag using AJAX endpoint
    """
    
    # The AJAX endpoint that loads the member list
    ajax_url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/440474-440474"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    print("Fetching member list from AJAX endpoint...")
    print(f"URL: {ajax_url}")
    
    response = requests.get(ajax_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return []
    
    # Save raw response
    with open('bundestag_ajax_response.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Saved AJAX response to bundestag_ajax_response.html")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    members_data = []
    
    # Look for member cards or links
    # Try different patterns
    all_links = soup.find_all('a', href=True)
    print(f"\nFound {len(all_links)} total links")
    
    # Find links with mdbId
    mdb_links = [link for link in all_links if 'mdbId=' in link.get('href', '')]
    print(f"Found {len(mdb_links)} links with mdbId")
    
    # Look for member cards/items
    for link in all_links:
        href = link.get('href', '')
        
        # Check if this is a member profile link
        if '/abgeordnete/' in href and 'biografien' in href:
            # Extract member info
            member_name = link.get_text(strip=True)
            
            # Find the parent container that might have more info
            parent = link.find_parent(['div', 'li', 'article', 'tr'])
            
            if parent:
                parent_text = parent.get_text()
                
                # Try to find PLZ (5-digit number)
                plz_matches = re.findall(r'\b(\d{5})\b', parent_text)
                plz = plz_matches[0] if plz_matches else None
                
                # Try to find mdbId in nearby elements
                mdb_id = None
                mdb_links_in_parent = parent.find_all('a', href=re.compile(r'mdbId=\d+'))
                if mdb_links_in_parent:
                    mdb_match = re.search(r'mdbId=(\d+)', mdb_links_in_parent[0].get('href'))
                    if mdb_match:
                        mdb_id = mdb_match.group(1)
                
                if mdb_id:
                    member_info = {
                        'name': member_name,
                        'mdbId': mdb_id,
                        'plz': plz,
                        'profile_url': f"https://www.bundestag.de{href}",
                        'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}"
                    }
                    
                    # Check if not duplicate
                    if not any(m['mdbId'] == mdb_id for m in members_data):
                        members_data.append(member_info)
                        print(f"Found: {member_name} (mdbId: {mdb_id}, PLZ: {plz})")
    
    # Also try to find direct contact links
    contact_links = soup.find_all('a', href=re.compile(r'contactform\?mdbId=\d+'))
    print(f"\nFound {len(contact_links)} direct contact links")
    
    for link in contact_links:
        href = link.get('href', '')
        mdb_match = re.search(r'mdbId=(\d+)', href)
        if mdb_match:
            mdb_id = mdb_match.group(1)
            
            # Find associated info
            parent = link.find_parent(['div', 'li', 'article', 'tr'])
            member_name = ""
            plz = None
            
            if parent:
                # Find name
                name_elem = parent.find(['h2', 'h3', 'h4', 'strong', 'b'])
                if name_elem:
                    member_name = name_elem.get_text(strip=True)
                
                # Find PLZ
                parent_text = parent.get_text()
                plz_matches = re.findall(r'\b(\d{5})\b', parent_text)
                plz = plz_matches[0] if plz_matches else None
            
            if mdb_id and not any(m['mdbId'] == mdb_id for m in members_data):
                member_info = {
                    'name': member_name or f"Member {mdb_id}",
                    'mdbId': mdb_id,
                    'plz': plz,
                    'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}"
                }
                members_data.append(member_info)
    
    return members_data


def try_member_search_api():
    """
    Try to find if there's a JSON API for member search
    """
    print("\n" + "="*60)
    print("Trying to find JSON API endpoint...")
    print("="*60)
    
    # Common API patterns
    api_urls = [
        "https://www.bundestag.de/api/v3/members",
        "https://www.bundestag.de/api/members",
        "https://www.bundestag.de/resource/blob/abgeordnete",
        "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/440474-440474?limit=1000",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    for url in api_urls:
        try:
            print(f"\nTrying: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                # Check if it's JSON
                try:
                    json_data = response.json()
                    print("✓ Got JSON response!")
                    print(f"Keys: {json_data.keys() if isinstance(json_data, dict) else 'Array'}")
                    return json_data
                except:
                    print(f"Response length: {len(response.text)} chars")
                    # Check if it has mdbId
                    if 'mdbId' in response.text:
                        print("✓ Contains mdbId!")
        except Exception as e:
            print(f"Error: {e}")
    
    return None


if __name__ == "__main__":
    # First try API
    api_data = try_member_search_api()
    
    # Then try AJAX scraping
    members = scrape_bundestag_members_ajax()
    
    if members:
        # Save to JSON
        with open('bundestag_members.json', 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)
        
        # Also save as CSV
        import csv
        with open('bundestag_members.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'mdbId', 'plz', 'contact_url'])
            writer.writeheader()
            writer.writerows(members)
        
        print(f"\n{'='*60}")
        print(f"SUCCESS: Extracted {len(members)} members")
        print(f"{'='*60}")
        print(f"\nSaved to:")
        print(f"  - bundestag_members.json")
        print(f"  - bundestag_members.csv")
        
        print(f"\nFirst 5 members:")
        for member in members[:5]:
            print(f"  {member['name']}: mdbId={member['mdbId']}, PLZ={member['plz']}")
    else:
        print("\n❌ No members extracted.")
        print("The page structure might have changed or uses more complex JavaScript.")
