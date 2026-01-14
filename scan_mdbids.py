import requests
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def check_mdb_id(mdb_id):
    """Check if a given mdbId is valid by testing the contact URL"""
    
    url = f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        # If status is 200 and content contains member info, it's valid
        if response.status_code == 200:
            # Check if the page contains actual member data
            content = response.text.lower()
            if 'abgeordnete' in content or 'kontaktformular' in content:
                # Try to extract name from the page
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for member name in title or headings
                title = soup.find('title')
                name = ""
                if title:
                    title_text = title.get_text()
                    # Extract name from title
                    if ' - ' in title_text:
                        name = title_text.split(' - ')[0].strip()
                
                # Also look for h1/h2
                if not name:
                    h1 = soup.find(['h1', 'h2'])
                    if h1:
                        name = h1.get_text(strip=True)
                
                return {
                    'mdbId': str(mdb_id),
                    'name': name,
                    'status': 'valid',
                    'contact_url': url
                }
        
        return None
        
    except Exception as e:
        return None


def scan_mdb_ids_range(start_id, end_id, max_workers=10):
    """
    Scan a range of mdbIds to find valid ones
    """
    
    print(f"\nScanning mdbIds from {start_id} to {end_id}...")
    print(f"Using {max_workers} parallel workers")
    
    valid_members = []
    checked = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_id = {
            executor.submit(check_mdb_id, mdb_id): mdb_id 
            for mdb_id in range(start_id, end_id + 1)
        }
        
        # Process as they complete
        for future in as_completed(future_to_id):
            checked += 1
            
            if checked % 100 == 0:
                print(f"  Checked: {checked}/{end_id - start_id + 1}, Found: {len(valid_members)}")
            
            result = future.result()
            if result:
                valid_members.append(result)
                print(f"  ✓ Found: {result['mdbId']} - {result['name']}")
    
    return valid_members


def smart_scan():
    """
    Smart scanning based on the IDs we already know
    """
    
    # From our scraping, we know IDs are in the range 1043000-1049000
    # Let's scan this range
    
    known_ids = [
        1043506, 1043648, 1043938, 1044222, 1044246, 1044508, 1044590,
        1044778, 1045428, 1045438, 1045450, 1045490, 1045736, 1045826,
        1046050, 1046072, 1046116, 1046720, 1047200, 1047252, 1047564,
        1047638, 1047674, 1048238, 1049236
    ]
    
    print("="*70)
    print("SMART BUNDESTAG MEMBER ID SCANNER")
    print("="*70)
    print(f"\nKnown IDs: {len(known_ids)}")
    print(f"ID Range: {min(known_ids)} to {max(known_ids)}")
    
    # Scan a reasonable range
    start_id = 1043000
    end_id = 1050000
    
    print(f"\nWill scan range: {start_id} to {end_id}")
    print(f"Total IDs to check: {end_id - start_id + 1}")
    
    input("\nPress Enter to start scanning (this will take a while)...")
    
    start_time = time.time()
    
    members = scan_mdb_ids_range(start_id, end_id, max_workers=20)
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*70}")
    print(f"SCAN COMPLETE")
    print(f"{'='*70}")
    print(f"Time elapsed: {elapsed:.1f} seconds")
    print(f"Found {len(members)} valid members")
    
    return members


if __name__ == "__main__":
    # Option 1: Quick test on known range
    print("Quick test mode: scanning small sample...")
    test_members = scan_mdb_ids_range(1046000, 1046200, max_workers=10)
    
    if test_members:
        print(f"\n✓ Test successful! Found {len(test_members)} members in sample range")
        
        # Save test results
        with open('bundestag_test_scan.json', 'w', encoding='utf-8') as f:
            json.dump(test_members, f, ensure_ascii=False, indent=2)
        
        print("\nSample results:")
        for m in test_members[:10]:
            print(f"  {m['mdbId']}: {m['name']}")
        
        # Ask if user wants full scan
        print("\n" + "="*70)
        response = input("\nRun full scan? This will take 10-20 minutes (y/n): ")
        
        if response.lower() == 'y':
            all_members = smart_scan()
            
            if all_members:
                # Save results
                with open('bundestag_all_members_scanned.json', 'w', encoding='utf-8') as f:
                    json.dump(all_members, f, ensure_ascii=False, indent=2)
                
                with open('bundestag_all_members_scanned.csv', 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['mdbId', 'name', 'contact_url'])
                    writer.writeheader()
                    writer.writerows(all_members)
                
                print(f"\n✓ Saved {len(all_members)} members")
                print("  - bundestag_all_members_scanned.json")
                print("  - bundestag_all_members_scanned.csv")
    else:
        print("\n❌ Test failed - no members found")
        print("The website structure might have changed or rate limiting is active")
