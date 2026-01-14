import requests
from bs4 import BeautifulSoup
import json
import re
import time

def scrape_bundestag_members():
    """
    Scrape mdbId and PLZ from Bundestag members page
    """
    base_url = "https://www.bundestag.de/abgeordnete"
    
    # First, let's try to get the page and inspect its structure
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("Fetching main page...")
    response = requests.get(base_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for member links that contain mdbId
    members_data = []
    
    # Try to find links with mdbId pattern
    links = soup.find_all('a', href=re.compile(r'mdbId=\d+'))
    print(f"Found {len(links)} links with mdbId")
    
    # Also look for any JSON data embedded in the page
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string and 'mdbId' in script.string:
            print("Found script with mdbId data")
            # Try to extract JSON data
            try:
                # Look for JSON patterns
                json_match = re.search(r'\{[^{}]*"mdbId"[^{}]*\}', script.string)
                if json_match:
                    print("Found JSON pattern:", json_match.group(0)[:200])
            except:
                pass
    
    # Look for member cards or list items
    member_elements = soup.find_all(['div', 'li', 'article'], class_=re.compile(r'member|abgeordnete|card', re.I))
    print(f"Found {len(member_elements)} potential member elements")
    
    # Try to find the member list endpoint
    # The page likely loads data via AJAX
    for link in links[:10]:  # Check first 10 links
        href = link.get('href', '')
        mdb_match = re.search(r'mdbId=(\d+)', href)
        if mdb_match:
            mdb_id = mdb_match.group(1)
            # Try to find PLZ nearby
            parent = link.find_parent()
            text = parent.get_text() if parent else ''
            plz_match = re.search(r'\b\d{5}\b', text)
            plz = plz_match.group(0) if plz_match else None
            
            member_name = link.get_text(strip=True)
            
            print(f"Member: {member_name}, mdbId: {mdb_id}, PLZ: {plz}")
            
            members_data.append({
                'name': member_name,
                'mdbId': mdb_id,
                'plz': plz
            })
    
    # Save the raw HTML for inspection
    with open('bundestag_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("\nSaved raw HTML to bundestag_page.html for inspection")
    
    return members_data


if __name__ == "__main__":
    members = scrape_bundestag_members()
    
    if members:
        # Save to JSON
        with open('bundestag_members.json', 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)
        
        print(f"\nExtracted {len(members)} members")
        print("\nFirst 5 members:")
        for member in members[:5]:
            print(f"  {member}")
    else:
        print("\nNo members extracted. The page might use dynamic loading.")
        print("You may need to use Selenium for JavaScript-rendered content.")
