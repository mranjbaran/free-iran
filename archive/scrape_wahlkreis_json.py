from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import json
import time
import csv

def scrape_wahlkreissuche():
    """
    Scrape the Wahlkreissuche page that has a JSON data file with all Wahlkreise
    """
    
    print("Starting Firefox...")
    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        # Navigate to Wahlkreissuche page
        url = "https://www.bundestag.de/parlament/wahlen/Wahlergebnisse"
        print(f"Loading {url}...")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Save page source
        with open('wahlkreissuche_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Saved page source to wahlkreissuche_page.html")
        
        # The page has a data-map-path-to-wkdata attribute with JSON file
        # data-map-path-to-wkdata="/static/appdata/includes/datasources/wahlkreisergebnisse/btwahl2025/wahlkreise.json"
        
        # Get all script tags and data attributes
        print("\nLooking for Wahlkreis data...")
        
        # Try to find the body element with data attributes
        body = driver.find_element(By.TAG_NAME, "body")
        wk_data_path = body.get_attribute("data-map-path-to-wkdata")
        
        if wk_data_path:
            print(f"Found Wahlkreis data path: {wk_data_path}")
            
            # Load the JSON data
            json_url = f"https://www.bundestag.de{wk_data_path}"
            print(f"Loading {json_url}...")
            driver.get(json_url)
            time.sleep(2)
            
            # Get the JSON content
            json_text = driver.find_element(By.TAG_NAME, "pre").text
            wahlkreise_data = json.loads(json_text)
            
            print(f"Found {len(wahlkreise_data)} Wahlkreise!")
            
            # Save to file
            with open('wahlkreise_complete.json', 'w', encoding='utf-8') as f:
                json.dump(wahlkreise_data, f, ensure_ascii=False, indent=2)
            
            print("Saved to wahlkreise_complete.json")
            
            # Parse and show sample
            print("\nSample Wahlkreise:")
            for i, wk in enumerate(wahlkreise_data[:5]):
                print(f"\nWahlkreis {wk.get('wahlkreis_nr', 'N/A')}:")
                print(f"  Name: {wk.get('wahlkreis_name', 'N/A')}")
                print(f"  Cities: {wk.get('cities', [])[:3]}")  # First 3 cities
                print(f"  Winner: {wk.get('winner_name', 'N/A')}")
            
            return wahlkreise_data
        else:
            print("Could not find Wahlkreis data path")
            return None
        
    finally:
        print("\nClosing browser...")
        driver.quit()


def map_plz_to_members():
    """
    Create a mapping from PLZ to members using Wahlkreis data
    """
    
    print("\n" + "="*70)
    print("Creating PLZ to Members mapping...")
    print("="*70)
    
    # Load complete member list
    members = {}
    with open('bundestag_complete.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            members[row['name']] = row
    
    print(f"Loaded {len(members)} members")
    
    # Load Wahlkreis data
    with open('wahlkreise_complete.json', 'r', encoding='utf-8') as f:
        wahlkreise = json.load(f)
    
    print(f"Loaded {len(wahlkreise)} Wahlkreise")
    
    # Create PLZ mapping
    plz_map = {}
    
    for wk in wahlkreise:
        wk_nr = wk.get('wahlkreis_nr')
        wk_name = wk.get('wahlkreis_name')
        cities = wk.get('cities', [])
        winner_name = wk.get('winner_name', '')
        
        # Note: The JSON likely has PLZ data in cities or separate field
        # Let's examine the structure
        
        if cities:
            for city_info in cities:
                if isinstance(city_info, dict):
                    city = city_info.get('name', '')
                    plz_list = city_info.get('plz', [])
                elif isinstance(city_info, str):
                    city = city_info
                    plz_list = []
                
                # Map each PLZ to this Wahlkreis
                for plz in plz_list:
                    if plz not in plz_map:
                        plz_map[plz] = []
                    
                    plz_map[plz].append({
                        'wahlkreis_nr': wk_nr,
                        'wahlkreis_name': wk_name,
                        'city': city,
                        'winner': winner_name
                    })
    
    print(f"Created mapping for {len(plz_map)} PLZ codes")
    
    # Save PLZ mapping
    with open('plz_to_wahlkreis.json', 'w', encoding='utf-8') as f:
        json.dump(plz_map, f, ensure_ascii=False, indent=2)
    
    print("Saved to plz_to_wahlkreis.json")
    
    # Test with PLZ 10961
    if '10961' in plz_map:
        print(f"\n✓ Found PLZ 10961:")
        for wk in plz_map['10961']:
            print(f"  Wahlkreis {wk['wahlkreis_nr']}: {wk['wahlkreis_name']}")
            print(f"  Winner: {wk['winner']}")
    else:
        print(f"\n✗ PLZ 10961 not found in mapping")
        
        # Show some sample PLZ for Berlin
        print("\nSample Berlin PLZ:")
        berlin_plz = [plz for plz in plz_map.keys() if plz.startswith('10') or plz.startswith('12') or plz.startswith('13')]
        for plz in sorted(berlin_plz)[:10]:
            print(f"  {plz}: {plz_map[plz][0]['wahlkreis_name']}")
    
    return plz_map


if __name__ == "__main__":
    # Step 1: Scrape Wahlkreis data
    wahlkreise = scrape_wahlkreissuche()
    
    if wahlkreise:
        # Step 2: Create PLZ mapping
        plz_map = map_plz_to_members()
