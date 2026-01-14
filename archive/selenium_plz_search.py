from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import json
import time

def search_plz_selenium(plz):
    """
    Use Selenium to interact with the PLZ search on Bundestag website
    """
    
    print(f"Starting Firefox...")
    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        # Navigate to Abgeordnete page
        url = "https://www.bundestag.de/abgeordnete"
        print(f"Loading {url}...")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Find PLZ input field
        print("Looking for PLZ input field...")
        
        # Try different possible selectors
        plz_input = None
        selectors = [
            "input[name='plz']",
            "input[id*='plz']",
            "input[placeholder*='PLZ']",
            "input[placeholder*='Postleitzahl']",
            ".ff-input-plz",
            "#ff-input-plz"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    plz_input = elements[0]
                    print(f"Found PLZ input with selector: {selector}")
                    break
            except:
                continue
        
        if not plz_input:
            # Print all input fields to debug
            print("\nAll input fields on page:")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for inp in inputs[:20]:  # First 20 inputs
                print(f"  Type: {inp.get_attribute('type')}, Name: {inp.get_attribute('name')}, "
                      f"ID: {inp.get_attribute('id')}, Placeholder: {inp.get_attribute('placeholder')}")
            
            # Save page source for debugging
            with open('abgeordnete_page_debug.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("Saved page source to abgeordnete_page_debug.html")
            
            return None
        
        # Enter PLZ
        print(f"Entering PLZ: {plz}")
        plz_input.clear()
        plz_input.send_keys(plz)
        time.sleep(2)
        
        # Look for autocomplete suggestions
        print("Looking for autocomplete suggestions...")
        autocomplete_selectors = [
            ".ui-autocomplete li",
            ".autocomplete-results li",
            "[role='option']",
            ".suggestion"
        ]
        
        suggestions = []
        for selector in autocomplete_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Found {len(elements)} suggestions with selector: {selector}")
                    for elem in elements:
                        suggestions.append({
                            'text': elem.text,
                            'value': elem.get_attribute('data-value') or elem.get_attribute('value')
                        })
                    break
            except:
                continue
        
        if suggestions:
            print(f"\nFound {len(suggestions)} autocomplete suggestions:")
            for sug in suggestions:
                print(f"  - {sug['text']}")
            
            # Click first suggestion
            print("\nClicking first suggestion...")
            elements[0].click()
            time.sleep(3)
        else:
            # Try submitting form
            print("No autocomplete found, trying to submit form...")
            try:
                submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
                submit_button.click()
                time.sleep(3)
            except:
                print("Could not find submit button")
        
        # Check for results
        print("\nLooking for results...")
        
        # Look for member cards/links
        member_elements = driver.find_elements(By.CSS_SELECTOR, ".bt-slide-content a[data-id], .col-xs-12.col-md-3 a[data-id]")
        
        if member_elements:
            print(f"Found {len(member_elements)} members!")
            
            members = []
            for elem in member_elements[:20]:  # First 20
                try:
                    mdb_id = elem.get_attribute('data-id')
                    name = elem.get_attribute('title')
                    
                    # Try to get fraktion
                    fraktion = ""
                    try:
                        fraktion_elem = elem.find_element(By.CSS_SELECTOR, ".bt-person-fraktion")
                        fraktion = fraktion_elem.text
                    except:
                        pass
                    
                    members.append({
                        'name': name,
                        'mdbId': mdb_id,
                        'fraktion': fraktion,
                        'contact_url': f'https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}'
                    })
                    
                    print(f"  - {name} ({fraktion}) [mdbId: {mdb_id}]")
                except Exception as e:
                    print(f"Error parsing member: {e}")
            
            # Save results
            result = {
                'plz': plz,
                'members': members
            }
            
            with open(f'plz_{plz}_results.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"\nSaved results to plz_{plz}_results.json")
            return result
        else:
            print("No member results found")
            
            # Save page source for debugging
            with open(f'plz_{plz}_page.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"Saved page source to plz_{plz}_page.html")
            
            return None
        
    finally:
        print("\nClosing browser...")
        driver.quit()


if __name__ == "__main__":
    # Test with PLZ 10961 (should return Pascal Meiser)
    result = search_plz_selenium('10961')
    
    if result and result['members']:
        print(f"\n{'='*70}")
        print(f"RESULTS FOR PLZ 10961:")
        print(f"{'='*70}")
        
        # Check if Pascal Meiser is in results
        found_meiser = False
        for member in result['members']:
            if 'Meiser' in member['name']:
                found_meiser = True
                print(f"✓ FOUND: {member['name']} ({member['fraktion']})")
            else:
                print(f"  {member['name']} ({member['fraktion']})")
        
        if not found_meiser:
            print("\n✗ Pascal Meiser NOT found in results")
    else:
        print("\n✗ No results found for PLZ 10961")
