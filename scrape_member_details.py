from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import json
import csv
import time

def scrape_member_details(mdb_id, name):
    """
    Scrape Wahlkreis and address info from a member's detail page
    """
    
    # Member's bio page URL
    url = f"https://www.bundestag.de/abgeordnete/biografien/{mdb_id}"
    
    print(f"Scraping {name} ({mdb_id})...")
    print(f"URL: {url}")
    
    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    options.add_argument('--headless')  # Run in background
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(3)
        
        # Extract Wahlkreis info
        wahlkreis = ""
        try:
            wk_elem = driver.find_element(By.CSS_SELECTOR, "[class*='wahlkreis']")
            wahlkreis = wk_elem.text
        except:
            # Try alternative selectors
            try:
                # Look for text containing "Wahlkreis"
                all_text = driver.find_element(By.TAG_NAME, "body").text
                lines = all_text.split('\n')
                for line in lines:
                    if 'Wahlkreis' in line:
                        wahlkreis = line
                        break
            except:
                pass
        
        # Extract address/PLZ info
        address_info = {}
        try:
            # Look for address blocks
            address_elems = driver.find_elements(By.CSS_SELECTOR, ".bt-address, [class*='address']")
            for elem in address_elems:
                text = elem.text
                if text:
                    # Parse address - typically has PLZ and city
                    lines = text.split('\n')
                    for line in lines:
                        # German PLZ are 5 digits
                        import re
                        plz_match = re.search(r'\b(\d{5})\b', line)
                        if plz_match:
                            address_info['plz'] = plz_match.group(1)
                            # City is usually after PLZ
                            city_match = re.search(r'\d{5}\s+(.+)', line)
                            if city_match:
                                address_info['city'] = city_match.group(1).strip()
                            break
        except:
            pass
        
        result = {
            'mdbId': mdb_id,
            'name': name,
            'wahlkreis': wahlkreis,
            'address': address_info
        }
        
        print(f"  Wahlkreis: {wahlkreis}")
        print(f"  Address: {address_info}")
        
        return result
        
    finally:
        driver.quit()


def scrape_all_members_details():
    """
    Scrape details for all members
    """
    
    print("="*70)
    print("SCRAPING MEMBER DETAILS")
    print("="*70)
    
    # Load member list
    members = []
    with open('bundestag_complete.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        members = list(reader)
    
    print(f"Found {len(members)} members to scrape")
    
    # First, test with Pascal Meiser
    meiser = [m for m in members if 'Meiser' in m['name']][0]
    
    print(f"\nTest scraping for Pascal Meiser:")
    result = scrape_member_details(meiser['mdbId'], meiser['name'])
    
    print(f"\nResult:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Ask if should continue
    print("\n" + "="*70)
    cont = input("Continue scraping all 634 members? This will take ~30 minutes (y/n): ")
    
    if cont.lower() != 'y':
        print("Stopped")
        return
    
    # Scrape all members
    all_results = []
    
    for i, member in enumerate(members):
        try:
            result = scrape_member_details(member['mdbId'], member['name'])
            all_results.append(result)
            
            # Save progress every 50 members
            if (i + 1) % 50 == 0:
                with open('member_details_progress.json', 'w', encoding='utf-8') as f:
                    json.dump(all_results, f, ensure_ascii=False, indent=2)
                print(f"\nProgress: {i+1}/{len(members)} members scraped")
            
            # Be nice to the server
            time.sleep(1)
            
        except Exception as e:
            print(f"Error scraping {member['name']}: {e}")
            continue
    
    # Save final results
    with open('member_details_complete.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print(f"Completed! Scraped {len(all_results)} members")
    print(f"{'='*70}")
    
    # Create PLZ mapping
    plz_map = {}
    for member in all_results:
        address = member.get('address', {})
        plz = address.get('plz')
        
        if plz:
            if plz not in plz_map:
                plz_map[plz] = []
            
            plz_map[plz].append({
                'name': member['name'],
                'mdbId': member['mdbId'],
                'fraktion': next((m['fraktion'] for m in members if m['mdbId'] == member['mdbId']), ''),
                'wahlkreis': member['wahlkreis'],
                'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={member['mdbId']}"
            })
    
    with open('plz_to_members.json', 'w', encoding='utf-8') as f:
        json.dump(plz_map, f, ensure_ascii=False, indent=2)
    
    print(f"Created PLZ mapping with {len(plz_map)} PLZ codes")
    
    # Test with 10961
    if '10961' in plz_map:
        print(f"\n✓ PLZ 10961 found!")
        for member in plz_map['10961']:
            print(f"  - {member['name']} ({member['fraktion']})")
    else:
        print(f"\n✗ PLZ 10961 not found")


if __name__ == "__main__":
    scrape_all_members_details()
