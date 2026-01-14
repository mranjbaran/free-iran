"""
Scrape all members' Wahlkreis by checking their profile pages
Uses requests (faster than Selenium)
"""

import csv
import json
import requests
import re
import time
from bs4 import BeautifulSoup

def get_wahlkreis_for_member(mdb_id, name):
    """
    Get Wahlkreis from member's profile page
    Returns: {'number': '082', 'name': 'Berlin-Friedrichshain-Kreuzberg – Prenzlauer Berg Ost'} or None
    """
    # Construct profile URL
    lastname = name.split(',')[0].split()[-1].lower()
    url = f"https://www.bundestag.de/abgeordnete/biografien/{lastname}-{mdb_id}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Search for Wahlkreis pattern
            # Format: "Wahlkreis 082: Berlin-Friedrichshain-Kreuzberg – Prenzlauer Berg Ost"
            pattern = r'Wahlkreis\s+(\d{1,3}):\s+([^<>"]+?)(?:<|"|\s*\()'
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            
            if matches:
                num, wk_name = matches[0]
                return {
                    'number': num.zfill(3),
                    'name': wk_name.strip()
                }
            else:
                # Try alternative pattern without colon
                pattern2 = r'Wahlkreis\s+(\d{1,3})\s+[–-]\s+([^<>"]+?)(?:<|")'
                matches2 = re.findall(pattern2, response.text, re.IGNORECASE)
                
                if matches2:
                    num, wk_name = matches2[0]
                    return {
                        'number': num.zfill(3),
                        'name': wk_name.strip()
                    }
        
        return None
        
    except Exception as e:
        print(f"      Error: {e}")
        return None

def scrape_all_wahlkreise():
    """
    Scrape Wahlkreis for all members
    """
    print("="*70)
    print("SCRAPING WAHLKREIS FOR ALL BUNDESTAG MEMBERS")
    print("="*70)
    
    # Load members
    members = []
    with open('bundestag_complete.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        members = list(reader)
    
    print(f"\nTotal members to process: {len(members)}")
    
    # Results
    success_count = 0
    fail_count = 0
    results = []
    
    # Process each member
    for i, member in enumerate(members, 1):
        print(f"\n[{i}/{len(members)}] {member['name']} ({member['fraktion']})")
        
        wahlkreis = get_wahlkreis_for_member(member['mdbId'], member['name'])
        
        if wahlkreis:
            print(f"   ✓ Wahlkreis {wahlkreis['number']}: {wahlkreis['name']}")
            member['wahlkreis_number'] = wahlkreis['number']
            member['wahlkreis_name'] = wahlkreis['name']
            success_count += 1
        else:
            print(f"   ✗ No Wahlkreis (probably list candidate)")
            member['wahlkreis_number'] = ''
            member['wahlkreis_name'] = 'Landesliste'
        results.append(member)
        
        # Save progress every 50 members
        if i % 50 == 0:
            save_progress(results, success_count, fail_count + len(members) - success_count, i)
        
        # Be respectful - small delay
        time.sleep(0.3)
    
    # Final save
    print("\n" + "="*70)
    print("SCRAPING COMPLETE!")
    print("="*70)
    save_progress(results, success_count, len(members) - success_count, len(members))
    
    return results

def save_progress(results, success, fail, processed):
    """
    Save results to files
    """
    # CSV
    with open('bundestag_complete_with_wahlkreis.csv', 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['name', 'mdbId', 'fraktion', 'wahlkreis_number', 'wahlkreis_name', 'contact_url']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    # JSON
    with open('bundestag_complete_with_wahlkreis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n>>> Progress saved:")
    print(f"    Processed: {processed} members")
    print(f"    With Wahlkreis: {success}")
    print(f"    Without Wahlkreis: {fail}")
    print(f"    Files: bundestag_complete_with_wahlkreis.csv/json")

if __name__ == "__main__":
    results = scrape_all_wahlkreise()
    
    # Summary
    with_wk = [m for m in results if m['wahlkreis_number']]
    without_wk = [m for m in results if not m['wahlkreis_number']]
    
    print(f"\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    print(f"Total members: {len(results)}")
    print(f"With Wahlkreis: {len(with_wk)} ({len(with_wk)/len(results)*100:.1f}%)")
    print(f"Without Wahlkreis (Landesliste): {len(without_wk)} ({len(without_wk)/len(results)*100:.1f}%)")
    
    # Show unique Wahlkreise
    wahlkreise = set((m['wahlkreis_number'], m['wahlkreis_name']) for m in with_wk if m['wahlkreis_number'])
    print(f"\nTotal unique Wahlkreise found: {len(wahlkreise)}")
