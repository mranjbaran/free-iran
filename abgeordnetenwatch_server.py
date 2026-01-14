"""
Flask server for Abgeordnetenwatch PLZ lookup
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import csv
import os
from gender_data import GENDER_LOOKUP

app = Flask(__name__)
CORS(app)

def normalize_name(name):
    """Normalize name by removing Dr. prefix and extra spaces"""
    import re
    # Remove Dr., dr., Dr, dr prefixes (with or without dot, with optional spaces)
    normalized = re.sub(r'\b[Dd][Rr]\.?\s+', '', name)
    # Remove extra spaces
    normalized = ' '.join(normalized.split())
    return normalized.strip()

def detect_gender(full_name):
    """Detect gender using comprehensive MP database"""
    # Normalize and try exact match (case-insensitive)
    normalized_name = normalize_name(full_name).lower()
    return GENDER_LOOKUP.get(normalized_name, 'unknown')

# Load contact URLs from CSV database
CONTACT_URL_MAP = {}
def load_contact_urls():
    csv_path = os.path.join('data', 'bundestag_contacts.csv')
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # CSV has names in "Last, First" format
                    # Store both formats for matching
                    name_csv = row['name'].strip()
                    
                    # Normalize name (remove Dr. prefix)
                    name_normalized = normalize_name(name_csv)
                    
                    # Store original format: "Meiser, Pascal"
                    name_key1 = name_normalized.lower()
                    CONTACT_URL_MAP[name_key1] = row['contact_url']
                    
                    # Also store reversed format: "Pascal Meiser"
                    if ',' in name_normalized:
                        parts = name_normalized.split(',', 1)
                        name_reversed = f"{parts[1].strip()} {parts[0].strip()}"
                        name_key2 = name_reversed.lower()
                        CONTACT_URL_MAP[name_key2] = row['contact_url']
                    
            print(f"✓ Loaded {len(CONTACT_URL_MAP)} contact URLs from database")
        except Exception as e:
            print(f"Warning: Could not load contact URLs: {e}")
    else:
        print("Warning: data/bundestag_contacts.csv not found")

load_contact_urls()

def scrape_abgeordnetenwatch_by_plz(plz):
    """
    Scrape MPs from abgeordnetenwatch.de for a given PLZ
    """
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
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        
        # CHECK IF MULTIPLE WAHLKREIS OPTIONS ARE SHOWN
        try:
            # Look for message indicating multiple results
            multi_result_msg = driver.find_element(By.XPATH, "//p[contains(text(), 'wurden mehrere Ergebnisse gefunden')]")
            if multi_result_msg:
                print("Multiple Wahlkreis options found")
                wahlkreis_options = []
                
                # Find all option tiles
                option_tiles = driver.find_elements(By.CSS_SELECTOR, "article.tile")
                
                for tile in option_tiles:
                    try:
                        title_elem = tile.find_element(By.CSS_SELECTOR, ".tile__title")
                        title = title_elem.text.strip()
                        
                        link_elem = tile.find_element(By.CSS_SELECTOR, ".tile__links a")
                        link = link_elem.get_attribute('href')
                        
                        wahlkreis_options.append({
                            'title': title,
                            'url': link
                        })
                        print(f"  Option: {title}")
                    except:
                        continue
                
                if wahlkreis_options:
                    return {
                        'type': 'multiple_wahlkreis',
                        'options': wahlkreis_options
                    }
        except:
            # Not a multiple result page, continue with normal scraping
            pass
        
        # Find all politician tiles
        politician_elements = driver.find_elements(By.CSS_SELECTOR, "article.tile--politician")
        print(f"Found {len(politician_elements)} politicians")
        
        politicians = []
        
        for element in politician_elements:
            try:
                mp_data = {}
                
                # Find name
                try:
                    name_div = element.find_element(By.CSS_SELECTOR, ".tile__politician__name")
                    mp_data['name'] = name_div.text.strip()
                except:
                    continue
                
                # Find profile URL
                try:
                    profile_link = element.find_element(By.CSS_SELECTOR, "a[href*='/profile/']")
                    href = profile_link.get_attribute('href')
                    if href.startswith('/'):
                        mp_data['profile_url'] = "https://www.abgeordnetenwatch.de" + href
                    else:
                        mp_data['profile_url'] = href
                except:
                    mp_data['profile_url'] = None
                
                # Find party
                try:
                    party_element = element.find_element(By.CSS_SELECTOR, ".tile__politician__party")
                    mp_data['party'] = party_element.text.strip()
                except:
                    mp_data['party'] = 'Unknown'
                
                # Find constituency
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
                                # Add contact URL from archived data (normalize name for matching)
                name_key = normalize_name(mp_data['name']).lower()
                mp_data['contact_url'] = CONTACT_URL_MAP.get(name_key, None)
                
                # Detect gender from name
                mp_data['gender'] = detect_gender(mp_data['name'])
                
                politicians.append(mp_data)
                print(f"✓ {mp_data['name']} ({mp_data['party']})")
            
            except Exception as e:
                print(f"Error extracting politician: {e}")
                continue
        
        return politicians
    
    finally:
        driver.quit()


@app.route('/api/search', methods=['GET'])
def search_plz():
    """
    API endpoint to search by PLZ
    """
    plz = request.args.get('plz', '').strip()
    
    if not plz:
        return jsonify({'error': 'PLZ parameter is required'}), 400
    
    if not plz.isdigit() or len(plz) != 5:
        return jsonify({'error': 'PLZ must be a 5-digit number'}), 400
    
    try:
        print(f"Searching for PLZ: {plz}")
        results = scrape_abgeordnetenwatch_by_plz(plz)
        
        # Check if results indicate multiple Wahlkreis options
        if isinstance(results, dict) and results.get('type') == 'multiple_wahlkreis':
            return jsonify({
                'plz': plz,
                'type': 'multiple_wahlkreis',
                'message': f'PLZ {plz} gehört zu mehreren Wahlkreisen',
                'options': results['options']
            })
        
        return jsonify({
            'plz': plz,
            'type': 'members',
            'count': len(results),
            'members': results
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("=" * 80)
    print("ABGEORDNETENWATCH FINDER - FLASK SERVER")
    print("=" * 80)
    print("\nStarting server on http://localhost:5000")
    print("API endpoint: http://localhost:5000/api/search?plz=<PLZ>")
    print("\nOpen abgeordnetenwatch_finder.html in your browser")
    print("=" * 80)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
