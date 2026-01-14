"""
Create accurate PLZ mapping - only map PLZ codes we can confidently determine
For others, use city name search
"""

import json
import csv
import re

# Load all members with Wahlkreis
members = []
with open('bundestag_complete_with_wahlkreis.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    members = list(reader)

# Get unique Wahlkreise
wahlkreise = {}
for member in members:
    if member['wahlkreis_number']:
        wk_num = member['wahlkreis_number']
        if wk_num not in wahlkreise:
            wahlkreise[wk_num] = {
                'number': wk_num,
                'name': member['wahlkreis_name'],
                'members': []
            }
        wahlkreise[wk_num]['members'].append({
            'name': member['name'],
            'mdbId': member['mdbId'],
            'fraktion': member['fraktion'],
            'contact_url': member['contact_url']
        })

print(f"Loaded {len(wahlkreise)} Wahlkreise")

# Only map specific PLZ ranges we can confidently determine
# Use narrower, more specific ranges for cities that have only ONE Wahlkreis
SPECIFIC_PLZ_MAPPINGS = {
    # Only map PLZ to Wahlkreis if the city/region has a SINGLE Wahlkreis
    # or if we can be very specific about the range
    
    # Single-Wahlkreis cities (more reliable)
    "Paderborn": (33098, 33129),
    "Bamberg": (96047, 96052),
    "Esslingen": (73728, 73760),
    "Calw": (72213, 72296),
    "Hanau": (63450, 63457),
    "Osnabrück": (49074, 49090),
    "Aachen": (52062, 52080),
    "Bielefeld": (33602, 33739),
    "Mannheim": (68159, 68309),
    "Offenbach": (63065, 63075),
    "Goslar": (38640, 38690),  # Includes Clausthal-Zellerfeld (38678)
}

PLZ_TO_WAHLKREIS = {}

# Map specific ranges
for city, (start, end) in SPECIFIC_PLZ_MAPPINGS.items():
    # Find the Wahlkreis for this city
    for wk_num, wk_data in wahlkreise.items():
        if city.lower() in wk_data['name'].lower():
            for plz in range(start, end + 1):
                plz_str = str(plz).zfill(5)
                PLZ_TO_WAHLKREIS[plz_str] = wk_num
            break

print(f"Mapped {len(PLZ_TO_WAHLKREIS)} specific PLZ codes")

# Create PLZ to members mapping (only verified codes)
plz_to_members = {}
for plz, wk_num in PLZ_TO_WAHLKREIS.items():
    if wk_num in wahlkreise:
        plz_to_members[plz] = {
            'wahlkreis_number': wk_num,
            'wahlkreis_name': wahlkreise[wk_num]['name'],
            'members': wahlkreise[wk_num]['members']
        }

# Also create a city search index
city_to_wahlkreis = {}
for wk_num, wk_data in wahlkreise.items():
    # Extract city names from Wahlkreis name
    wk_name = wk_data['name']
    # Split by common separators
    parts = re.split(r'[–—-]\s+|\s+[–—-]\s+', wk_name)
    for part in parts:
        # Clean up
        part = part.strip()
        # Remove Roman numerals and parentheses
        part = re.sub(r'\s+[IVX]+$', '', part)
        part = re.sub(r'\s*\(.*?\)', '', part)
        
        # Also extract individual words (for cases like "Goslar – Northeim – Göttingen")
        words = part.split()
        for word in words:
            word = word.strip()
            if len(word) > 3:  # Only meaningful names
                word_lower = word.lower()
                if word_lower not in city_to_wahlkreis:
                    city_to_wahlkreis[word_lower] = []
                if wk_num not in city_to_wahlkreis[word_lower]:
                    city_to_wahlkreis[word_lower].append(wk_num)
        
        if len(part) > 3:  # Only meaningful names
            part_lower = part.lower()
            if part_lower not in city_to_wahlkreis:
                city_to_wahlkreis[part_lower] = []
            if wk_num not in city_to_wahlkreis[part_lower]:
                city_to_wahlkreis[part_lower].append(wk_num)

# Save files
with open('plz_to_members.json', 'w', encoding='utf-8') as f:
    json.dump(plz_to_members, f, indent=2, ensure_ascii=False)

# Save Wahlkreis list for city search
wahlkreis_list = []
for wk_num, wk_data in wahlkreise.items():
    wahlkreis_list.append({
        'number': wk_num,
        'name': wk_data['name'],
        'members': wk_data['members']
    })

with open('wahlkreis_list.json', 'w', encoding='utf-8') as f:
    json.dump(wahlkreis_list, f, indent=2, ensure_ascii=False)

print(f"\nSaved:")
print(f"  - plz_to_members.json ({len(plz_to_members)} verified PLZ codes)")
print(f"  - wahlkreis_list.json ({len(wahlkreis_list)} Wahlkreise for city search)")

# Test
print("\n" + "="*70)
print("TESTING")
print("="*70)

test_cases = [
    ("72213", True),
    ("73734", True),
    ("63549", True),
    ("33102", True),
    ("38678", True),  # Clausthal-Zellerfeld (Goslar)
    ("07907", False),  # Should NOT be mapped (ambiguous region)
    ("99634", False),  # Should NOT be mapped (ambiguous region)
]

for plz, should_find in test_cases:
    found = plz in plz_to_members
    status = "✓" if found == should_find else "✗"
    
    if found:
        data = plz_to_members[plz]
        print(f"{status} PLZ {plz}: Found → WK {data['wahlkreis_number']} {data['wahlkreis_name']}")
    else:
        print(f"{status} PLZ {plz}: Not mapped (user should search by city name)")

print("\n" + "="*70)
print(f"Strategy: Only map {len(plz_to_members)} verified PLZ codes")
print(f"For other PLZ, users can search by city/region name")
print("="*70)
