from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import json
import time
import re

def scrape_all_wahlkreise():
    """
    Scrape ALL Wahlkreise with members and PLZ information
    """
    
    print("="*70)
    print("SCRAPING ALL WAHLKREISE DATA")
    print("="*70)
    
    firefox_options = Options()
    firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    # firefox_options.add_argument('--headless')  # Uncomment for background mode
    
    print("\nInitializing Firefox...")
    try:
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
    except:
        driver = webdriver.Firefox(options=firefox_options)
    
    driver.maximize_window()
    all_wahlkreise = {}
    
    try:
        # Go to the Wahlkreis search page
        url = "https://www.bundestag.de/abgeordnete"
        print(f"\nLoading: {url}")
        driver.get(url)
        
        wait = WebDriverWait(driver, 20)
        time.sleep(5)
        
        # Look for PLZ input field
        print("\nLooking for PLZ search field...")
        
        # Try to find and use the PLZ/Ort search
        try:
            # Find the PLZ/Ort input field
            plz_inputs = driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='PLZ'], input[type='text']")
            
            for inp in plz_inputs:
                placeholder = inp.get_attribute('placeholder') or ''
                if 'PLZ' in placeholder or 'Ort' in placeholder:
                    print(f"Found PLZ input: {placeholder}")
                    plz_input = inp
                    break
            
        except Exception as e:
            print(f"Could not find PLZ input: {e}")
        
        # Alternative: Get the filter data directly from page source
        print("\nExtracting Wahlkreis data from page...")
        
        # Save page source for analysis
        with open('abgeordnete_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        print("Saved page source to abgeordnete_page.html")
        
        # Try to find the filterlist URL or data
        page_source = driver.page_source
        
        # Look for data-url or similar
        ajax_urls = re.findall(r'data-url="([^"]*filterlist[^"]*)"', page_source)
        if ajax_urls:
            print(f"Found {len(ajax_urls)} AJAX URLs")
            for url in ajax_urls[:3]:
                print(f"  - {url}")
        
    finally:
        print("\nClosing browser...")
        driver.quit()
    
    return all_wahlkreise


def use_bundestag_plz_api(plz):
    """
    Try to use Bundestag's PLZ search API directly
    """
    import requests
    from bs4 import BeautifulSoup
    
    # Try the search by PLZ
    search_url = f"https://www.bundestag.de/ajax/filterlist/de/abgeordnete/440474-440474/plz-{plz}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html',
        'Referer': 'https://www.bundestag.de/abgeordnete'
    }
    
    print(f"\nTrying PLZ search API: {plz}")
    print(f"URL: {search_url}")
    
    response = requests.get(search_url, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save response
        with open(f'plz_{plz}_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Response length: {len(response.text)} chars")
        
        # Look for member data
        member_links = soup.find_all('a', attrs={'data-id': True})
        print(f"Found {len(member_links)} members")
        
        return response.text
    
    return None


if __name__ == "__main__":
    # First try direct PLZ API
    print("Testing PLZ search functionality...")
    
    test_plzs = ['10961', '10115', '80331', '50667']
    
    for plz in test_plzs:
        result = use_bundestag_plz_api(plz)
        if result:
            print(f"✓ PLZ {plz} search worked!")
        else:
            print(f"✗ PLZ {plz} search failed")
        print()
    
    # Then try full scrape
    print("\n" + "="*70)
    input("Press Enter to start full Wahlkreis scraping...")
    scrape_all_wahlkreise()
