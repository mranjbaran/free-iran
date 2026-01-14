"""
Quick test: Get Pascal Meiser's Wahlkreis by scraping his profile page
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
import re

def test_meiser():
    # Setup Firefox
    firefox_binary = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_binary
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        # Pascal Meiser's profile URL
        # mdbId: 1046050
        # Format: https://www.bundestag.de/abgeordnete/biografien/{lastname}-{mdbId}
        
        url = "https://www.bundestag.de/abgeordnete/biografien/meiser-1046050"
        print(f"Loading Pascal Meiser's profile: {url}\n")
        
        driver.get(url)
        time.sleep(3)
        
        # Get page text
        page_text = driver.page_source
        
        # Save for inspection
        with open('meiser_profile.html', 'w', encoding='utf-8') as f:
            f.write(page_text)
        print("Saved page to meiser_profile.html")
        
        # Search for Wahlkreis
        print("\n" + "="*70)
        print("SEARCHING FOR WAHLKREIS INFORMATION")
        print("="*70)
        
        # Pattern 1: "Wahlkreis 083" format
        pattern1 = re.findall(r'Wahlkreis\s+(\d{1,3})', page_text, re.IGNORECASE)
        if pattern1:
            print(f"\n✓ Found Wahlkreis number(s): {pattern1}")
        
        # Pattern 2: Full Wahlkreis with name
        pattern2 = re.findall(r'Wahlkreis\s+(\d{1,3})\s+[–-]\s+([^\n<>"]+)', page_text, re.IGNORECASE)
        if pattern2:
            print(f"\n✓ Found full Wahlkreis info:")
            for num, name in pattern2:
                print(f"   Wahlkreis {num} - {name.strip()}")
        
        # Pattern 3: Just city names that might indicate district
        berlin_districts = re.findall(r'(Berlin-[A-Z][a-zäöüß-]+)', page_text)
        if berlin_districts:
            print(f"\n✓ Found Berlin district mentions: {set(berlin_districts)}")
        
        # Pattern 4: Search visible text for "083"
        if '083' in page_text:
            print(f"\n✓ Found '083' in page")
            # Get context around it
            idx = page_text.find('083')
            context = page_text[max(0, idx-100):idx+100]
            print(f"   Context: ...{context}...")
        
        print("\n" + "="*70)
        print("Press Enter to close browser...")
        input()
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_meiser()
