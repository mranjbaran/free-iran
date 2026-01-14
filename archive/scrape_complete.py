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

def scrape_all_bundestag_members():
    """
    Scrape ALL Bundestag members by navigating through all pages
    """
    
    print("="*70)
    print("SCRAPING ALL BUNDESTAG MEMBERS - COMPLETE VERSION")
    print("="*70)
    
    # Setup Firefox options
    firefox_options = Options()
    # Don't use headless - we need to see what's happening
    # firefox_options.add_argument('--headless')
    firefox_options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    
    # Initialize driver
    print("\nInitializing Firefox driver...")
    try:
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
    except Exception as e:
        print(f"Error: {e}")
        print("Trying without webdriver-manager...")
        driver = webdriver.Firefox(options=firefox_options)
    
    driver.maximize_window()
    all_members = {}
    
    try:
        # Load the biografien page
        url = "https://www.bundestag.de/abgeordnete/biografien"
        print(f"\nLoading page: {url}")
        driver.get(url)
        
        # Wait for the slider to load
        print("Waiting for content to load...")
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bt-slider")))
        time.sleep(5)
        
        # Find total count
        try:
            slider = driver.find_element(By.CSS_SELECTOR, ".bt-slider")
            total_count = slider.get_attribute("data-allitemcount")
            print(f"Total members to extract: {total_count}")
        except:
            total_count = "Unknown"
        
        # Find pagination
        try:
            pagination_text = driver.find_element(By.CSS_SELECTOR, ".bt-slider-index").text
            print(f"Pagination: {pagination_text}")
            match = re.search(r'(\d+) von (\d+)', pagination_text)
            if match:
                total_pages = int(match.group(2))
                print(f"Total pages to navigate: {total_pages}")
            else:
                total_pages = 60  # Default to safe number
        except:
            total_pages = 60
            print(f"Could not find pagination, will try up to {total_pages} pages")
        
        # Navigate through all pages
        print(f"\n{'='*70}")
        print("Starting page navigation...")
        print(f"{'='*70}\n")
        
        for page_num in range(1, total_pages + 1):
            print(f"Page {page_num}/{total_pages}:", end=" ")
            
            # Wait a moment for page to stabilize
            time.sleep(2)
            
            # Extract members from current view
            try:
                member_links = driver.find_elements(By.CSS_SELECTOR, "a[data-id]")
                page_members = 0
                
                for link in member_links:
                    try:
                        mdb_id = link.get_attribute('data-id')
                        if not mdb_id or mdb_id in all_members:
                            continue
                        
                        name = link.get_attribute('title') or link.text.strip()
                        
                        # Try to find fraktion
                        fraktion = ""
                        try:
                            fraktion_elem = link.find_element(By.CSS_SELECTOR, ".bt-person-fraktion")
                            fraktion = fraktion_elem.text.strip()
                        except:
                            pass
                        
                        all_members[mdb_id] = {
                            'name': name,
                            'mdbId': mdb_id,
                            'fraktion': fraktion,
                            'contact_url': f"https://www.bundestag.de/services/formular/contactform?mdbId={mdb_id}"
                        }
                        page_members += 1
                        
                    except Exception as e:
                        continue
                
                print(f"Extracted {page_members} new members (Total: {len(all_members)})")
                
            except Exception as e:
                print(f"Error extracting: {e}")
            
            # Check if we should continue
            if page_num >= total_pages:
                print("\nReached last page")
                break
            
            # Try to click next button
            try:
                # Find the next button
                next_button = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.slick-next:not(.slick-disabled)")
                ))
                
                # Scroll into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                time.sleep(0.5)
                
                # Click
                next_button.click()
                time.sleep(1)
                
            except Exception as e:
                print(f"\nCannot click next button: {e}")
                print("This might be the last page")
                break
        
        print(f"\n{'='*70}")
        print(f"Extraction complete!")
        print(f"{'='*70}")
        
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\nClosing browser...")
        driver.quit()
    
    return list(all_members.values())


if __name__ == "__main__":
    members = scrape_all_bundestag_members()
    
    if members:
        # Sort by name
        members.sort(key=lambda x: x.get('name', ''))
        
        print(f"\n{'='*70}")
        print(f"✓✓✓ SUCCESS: {len(members)} members extracted ✓✓✓")
        print(f"{'='*70}")
        
        # Save to JSON
        with open('bundestag_complete.json', 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)
        
        # Save to CSV
        with open('bundestag_complete.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'mdbId', 'fraktion', 'contact_url'])
            writer.writeheader()
            writer.writerows(members)
        
        # Simple text list
        with open('bundestag_mdbid_list.txt', 'w', encoding='utf-8') as f:
            f.write("Name,mdbId,Fraktion,Contact_URL\n")
            for m in members:
                f.write(f"{m.get('name', 'N/A')},{m['mdbId']},{m.get('fraktion', 'N/A')},{m['contact_url']}\n")
        
        print(f"\n📄 Files created:")
        print(f"  - bundestag_complete.json")
        print(f"  - bundestag_complete.csv")
        print(f"  - bundestag_mdbid_list.txt")
        
        print(f"\n📊 Sample (first 20 members):")
        for i, m in enumerate(members[:20], 1):
            print(f"{i:3}. {m.get('name', 'N/A'):40} {m.get('fraktion', 'N/A'):25} mdbId: {m['mdbId']}")
        
        # Stats
        print(f"\n📈 Statistics:")
        print(f"  Total members: {len(members)}")
        
        # Count by Fraktion
        fraktionen = {}
        for m in members:
            frak = m.get('fraktion', 'Unknown').strip()
            if frak:
                fraktionen[frak] = fraktionen.get(frak, 0) + 1
        
        print(f"\n  By Fraktion:")
        for frak, count in sorted(fraktionen.items(), key=lambda x: -x[1]):
            print(f"    {frak:30}: {count}")
        
    else:
        print("\n❌ No members extracted")
