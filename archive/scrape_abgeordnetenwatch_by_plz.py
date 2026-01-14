"""
Abgeordnetenwatch.de PLZ Scraper
Scrapes Bundestag MPs by postal code from abgeordnetenwatch.de
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import json
import time

def scrape_abgeordnetenwatch_by_plz(plz):
    """
    Scrape MPs from abgeordnetenwatch.de for a given PLZ
    
    Args:
        plz (str): German postal code (5 digits)
    
    Returns:
        list: List of MPs with their details
    """
    
    # Construct the search URL
    base_url = "https://www.abgeordnetenwatch.de/bundestag/abgeordnete"
    params = {
        'politician_search_keys': plz,
        'fraction': 'All',
        'constituency': 'All',
        'electoral_list': 'All',
        'candidacy_mandate_status_with_context': 'current_last'
    }
    
    url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    print(f"Scraping: {url}")
    
    # Setup Firefox with headless mode
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    
    driver = webdriver.Firefox(options=firefox_options)
    
    try:
        # Load the page
        driver.get(url)
        
        # Wait for results to load (wait for politician cards)
        print("Waiting for page to load...")
        time.sleep(3)  # Give page time to render
        
        # Try to find politician cards
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "politician-card"))
            )
        except:
            print("No politician cards found, trying alternative selectors...")
        
        # Get page source for debugging
        page_source = driver.page_source
        
        # Find all politician entries
        politicians = []
        
        # The correct selector for abgeordnetenwatch.de
        try:
            politician_elements = driver.find_elements(By.CSS_SELECTOR, "article.tile--politician")
            print(f"Found {len(politician_elements)} politician tiles")
        except Exception as e:
            print(f"Error finding politician elements: {e}")
            politician_elements = []
        
        if not politician_elements:
            print("No politician elements found. Saving page source for debugging...")
            with open(f'abgeordnetenwatch_debug_{plz}.html', 'w', encoding='utf-8') as f:
                f.write(page_source)
            print(f"Page source saved to abgeordnetenwatch_debug_{plz}.html")
            return []
        
        # Extract data from each politician card
        for element in politician_elements:
            try:
                mp_data = {}
                
                # Find name (it's in a div, not in a link)
                try:
                    name_div = element.find_element(By.CSS_SELECTOR, ".tile__politician__name")
                    mp_data['name'] = name_div.text.strip()
                except Exception as e:
                    print(f"Could not find name: {e}")
                    continue
                
                # Find profile URL (from the parent link)
                try:
                    profile_link = element.find_element(By.CSS_SELECTOR, "a[href*='/profile/']")
                    href = profile_link.get_attribute('href')
                    if href.startswith('/'):
                        mp_data['profile_url'] = "https://www.abgeordnetenwatch.de" + href
                    else:
                        mp_data['profile_url'] = href
                except:
                    mp_data['profile_url'] = None
                
                # Find party/fraction
                try:
                    party_element = element.find_element(By.CSS_SELECTOR, ".tile__politician__party")
                    mp_data['party'] = party_element.text.strip()
                except:
                    mp_data['party'] = 'Unknown'
                
                # Find constituency info
                try:
                    constituency_element = element.find_element(By.CSS_SELECTOR, ".politician-tile__candidacy-mandate-constituency")
                    mp_data['constituency'] = constituency_element.text.strip()
                except:
                    mp_data['constituency'] = 'N/A'
                
                # Find image
                try:
                    img_element = element.find_element(By.CSS_SELECTOR, ".tile__politician__image img")
                    src = img_element.get_attribute('src')
                    if src.startswith('/'):
                        mp_data['image_url'] = "https://www.abgeordnetenwatch.de" + src
                    else:
                        mp_data['image_url'] = src
                except:
                    mp_data['image_url'] = None
                
                politicians.append(mp_data)
                print(f"✓ {mp_data['name']} ({mp_data['party']})")
            
            except Exception as e:
                print(f"Error extracting politician data: {e}")
                continue
        
        return politicians
    
    finally:
        driver.quit()


def main():
    """Test the scraper with sample PLZ codes"""
    
    print("=" * 80)
    print("ABGEORDNETENWATCH PLZ SCRAPER")
    print("=" * 80)
    
    # Test with multiple PLZ codes
    test_plz_codes = ["33098", "10961", "72213", "38678"]
    
    all_results = {}
    
    for plz in test_plz_codes:
        print(f"\n{'=' * 80}")
        print(f"Testing PLZ: {plz}")
        print(f"{'=' * 80}")
        
        try:
            results = scrape_abgeordnetenwatch_by_plz(plz)
            all_results[plz] = results
            
            if results:
                print(f"\n✓ Found {len(results)} MP(s) for PLZ {plz}:")
                for mp in results:
                    print(f"\n  Name: {mp.get('name', 'N/A')}")
                    print(f"  Party: {mp.get('party', 'N/A')}")
                    print(f"  Constituency: {mp.get('constituency', 'N/A')}")
                    print(f"  Profile: {mp.get('profile_url', 'N/A')}")
                    print(f"  Image: {mp.get('image_url', 'N/A')}")
            else:
                print(f"\n✗ No MPs found for PLZ {plz}")
        
        except Exception as e:
            print(f"Error scraping PLZ {plz}: {e}")
            all_results[plz] = []
        
        time.sleep(2)  # Be nice to the server
    
    # Save results
    output_file = 'abgeordnetenwatch_scrape_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 80}")
    print(f"Results saved to {output_file}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
