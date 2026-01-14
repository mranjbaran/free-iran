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
import re

def scrape_all_members_selenium():
    """
    Use Selenium to scrape all members from the biografien page
    """
    
    print("="*70)
    print("SCRAPING ALL BUNDESTAG MEMBERS WITH SELENIUM (Firefox)")
    print("="*70)
    
    # Setup Firefox options
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Run in background
    firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    # Initialize driver
    print("\nInitializing Firefox driver...")
    try:
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
    except Exception as e:
        print(f"Error initializing driver with webdriver-manager: {e}")
        print("Trying without webdriver-manager...")
        driver = webdriver.Firefox(options=firefox_options)
    
    all_members = {}
    
    try:
        # Load the biografien page
        url = "https://www.bundestag.de/abgeordnete/biografien"
        print(f"\nLoading page: {url}")
        driver.get(url)
        
        # Wait for page to load
        print("Waiting for content to load...")
        time.sleep(5)
        
        # Find total number of pages
        total_pages = 1
        try:
            pagination_text = driver.find_element(By.CSS_SELECTOR, ".bt-slider-index").text
            print(f"Pagination: {pagination_text}")
            # Extract total pages from "1 von 53" format
            match = re.search(r'(\d+) von (\d+)', pagination_text)
            if match:
                current_page = int(match.group(1))
                total_pages = int(match.group(2))
                print(f"Total pages: {total_pages}")
        except Exception as e:
            print(f"Could not find pagination: {e}, assuming single page")
        
        # Click through all pages
        print(f"\nNavigating through {total_pages} pages...")
        for page in range(1, total_pages + 1):
            print(f"  Processing page {page}/{total_pages}...")
            time.sleep(2)  # Wait for content to load
            
            # Scroll to make sure all elements are visible
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            
            # Extract members from current page
            page_members = driver.find_elements(By.CSS_SELECTOR, "a[data-id]")
            print(f"    Found {len(page_members)} member elements on this page")
            
            # If not last page, click "Vor" (next) button
            if page < total_pages:
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button.slick-next:not(.slick-disabled)")
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(0.5)
                    next_button.click()
                    time.sleep(1)
                except Exception as e:
                    print(f"    Could not click next button: {e}")
                    break
        
        # Get page source
        html = driver.page_source
        
        # Save for inspection
        with open('biografien_selenium.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Saved page source to biografien_selenium.html")
        
        # Find all member links with data-id
        print("\nExtracting member data...")
        
        # Method 1: Find by data-id attribute
        member_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-id]")
        print(f"Found {len(member_elements)} elements with data-id")
        
        for elem in member_elements:
            try:
                mdb_id = elem.get_attribute('data-id')
                if not mdb_id or mdb_id in all_members:
                    continue
                
                name = elem.get_attribute('title') or elem.text.strip()
                
                # Try to find fraktion
                fraktion = ""
                try:
                    fraktion_elem = elem.find_element(By.CSS_SELECTOR, ".bt-person-fraktion")
                    fraktion = fraktion_elem.text.strip()
                except:
                    pass
                
                all_members[mdb_id] = {
                    'name': name,
                    'mdbId': mdb_id,
                    'fraktion': fraktion,
                    'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}"
                }
                
            except Exception as e:
                continue
        
        # Method 2: Find biography links
        bio_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/abgeordnete/biografien/']")
        print(f"Found {len(bio_links)} biography links")
        
        for link in bio_links:
            try:
                href = link.get_attribute('href')
                if not href:
                    continue
                
                # Extract mdbId from URL (last number)
                mdb_match = re.search(r'-(\d+)$', href)
                if mdb_match:
                    mdb_id = mdb_match.group(1)
                    
                    if mdb_id not in all_members:
                        name = link.text.strip() or link.get_attribute('title') or ""
                        
                        all_members[mdb_id] = {
                            'name': name,
                            'mdbId': mdb_id,
                            'fraktion': '',
                            'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}",
                            'profile_url': href
                        }
            except:
                continue
        
        print(f"\nExtracted {len(all_members)} unique members")
        
    finally:
        driver.quit()
        print("Browser closed")
    
    return list(all_members.values())


if __name__ == "__main__":
    members = scrape_all_members_selenium()
    
    if members:
        # Sort by name
        members.sort(key=lambda x: x.get('name', ''))
        
        print(f"\n{'='*70}")
        print(f"✓ SUCCESS: {len(members)} members extracted")
        print(f"{'='*70}")
        
        # Save to JSON
        with open('bundestag_all_members.json', 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)
        
        # Save to CSV
        with open('bundestag_all_members.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'mdbId', 'fraktion', 'contact_url'], extrasaction='ignore')
            writer.writeheader()
            writer.writerows(members)
        
        # Simple list
        with open('mdbid_contact_list.txt', 'w', encoding='utf-8') as f:
            f.write("mdbId,Name,Contact_URL\n")
            for m in members:
                f.write(f"{m['mdbId']},{m.get('name', 'N/A')},{m['contact_url']}\n")
        
        print(f"\n📄 Files created:")
        print(f"  - bundestag_all_members.json")
        print(f"  - bundestag_all_members.csv")
        print(f"  - mdbid_contact_list.txt")
        
        print(f"\n📊 Sample (first 15 members):")
        for i, m in enumerate(members[:15], 1):
            print(f"{i:2}. {m.get('name', 'N/A'):40} mdbId: {m['mdbId']}")
        
        # Stats
        if members:
            with_fraktion = len([m for m in members if m.get('fraktion')])
            print(f"\n📈 Statistics:")
            print(f"  Total members: {len(members)}")
            print(f"  With Fraktion info: {with_fraktion}")
    else:
        print("\n❌ No members extracted")
