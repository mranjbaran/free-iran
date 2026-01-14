from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import json
import time

def get_plz_mapping_selenium():
    """
    Use Selenium to interact with the PLZ search on Bundestag website
    """
    
    firefox_options = Options()
    firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    
    driver = webdriver.Firefox(options=firefox_options)
    driver.maximize_window()
    
    plz_to_wahlkreis = {}
    
    try:
        # Go to the Wahlkreissuche page
        url = "https://www.bundestag.de/abgeordnete"
        print(f"Loading: {url}")
        driver.get(url)
        
        wait = WebDriverWait(driver, 20)
        time.sleep(5)
        
        # Test PLZ: 10961 (should return Pascal Meiser)
        test_plzs = ["10961", "10115", "50667", "80331", "20095"]
        
        for plz in test_plzs:
            print(f"\n{'='*60}")
            print(f"Testing PLZ: {plz}")
            print(f"{'='*60}")
            
            # Find PLZ input field
            try:
                # Try different possible selectors
                plz_input = None
                selectors = [
                    "input[name='plz']",
                    "input[placeholder*='PLZ']",
                    "input[type='text'][id*='plz']",
                    "input[type='search'][name*='plz']"
                ]
                
                for selector in selectors:
                    try:
                        plz_input = driver.find_element(By.CSS_SELECTOR, selector)
                        print(f"✓ Found PLZ input with selector: {selector}")
                        break
                    except:
                        continue
                
                if not plz_input:
                    # Try finding by text near input
                    print("Trying to find PLZ input by searching page text...")
                    inputs = driver.find_elements(By.TAG_NAME, "input")
                    print(f"Found {len(inputs)} input fields total")
                    for inp in inputs[:20]:
                        inp_type = inp.get_attribute('type')
                        inp_name = inp.get_attribute('name')
                        inp_id = inp.get_attribute('id')
                        inp_placeholder = inp.get_attribute('placeholder')
                        print(f"  Input: type={inp_type}, name={inp_name}, id={inp_id}, placeholder={inp_placeholder}")
                    
                    print("\nLet me save the page HTML...")
                    with open('plz_search_page.html', 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    print("Saved to plz_search_page.html")
                    
                    input("\nPress Enter to continue (so you can inspect the browser)...")
                    break
                
                # Clear and enter PLZ
                plz_input.clear()
                plz_input.send_keys(plz)
                time.sleep(1)
                plz_input.send_keys(Keys.RETURN)
                time.sleep(3)
                
                # Get results
                print("Searching for results...")
                
                # Save current page
                with open(f'plz_results_{plz}.html', 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                print(f"Saved results to plz_results_{plz}.html")
                
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
                
                # Save page for debugging
                with open(f'error_page_{plz}.html', 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                print(f"Saved error page to error_page_{plz}.html")
                break
    
    finally:
        print("\nClosing browser...")
        driver.quit()
    
    return plz_to_wahlkreis


if __name__ == "__main__":
    print("Testing PLZ search with Selenium...")
    mapping = get_plz_mapping_selenium()
    
    print(f"\n\nFound {len(mapping)} PLZ mappings")
    
    if mapping:
        with open('plz_mapping_test.json', 'w', encoding='utf-8') as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
        print("Saved to plz_mapping_test.json")
