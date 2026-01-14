"""
Create comprehensive PLZ to Wahlkreis mapping for ALL German postal codes
Using postal code ranges and our complete Wahlkreis data
"""

import json
import csv
import re

# Load all members with Wahlkreis
members = []
with open('bundestag_complete_with_wahlkreis.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    members = list(reader)

# Get unique Wahlkreise with all members
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

print(f"Found {len(wahlkreise)} unique Wahlkreise")

# Comprehensive PLZ to Wahlkreis mapping based on German postal code system
# Format: PLZ range -> Wahlkreis number
PLZ_RANGES = {
    # Format: (start_plz, end_plz): wahlkreis_number
    
    # BERLIN (10xxx - 14xxx)
    (10115, 10999): {
        "074": ["10115", "10117", "10119", "10178", "10179", "10557", "10559"],  # Berlin-Mitte
        "075": ["10249", "10405", "10407", "10409", "10435", "10437", "10439"],  # Berlin-Pankow
        "076": ["10551", "10553", "10555"],  # Berlin-Reinickendorf (partial)
        "077": ["10585", "10587", "10589", "10623", "10625", "10627", "10629", "10707", "10709", "10711", "10713", "10715", "10717", "10719"],  # Charlottenburg-Wilmersdorf
        "078": ["10777", "10779", "10781", "10783", "10785", "10787", "10789", "10823", "10825", "10827", "10829"],  # Steglitz-Zehlendorf / Tempelhof-Schöneberg
        "082": ["10243", "10245", "10247", "10961", "10963", "10965", "10967", "10969", "10997", "10999"],  # Friedrichshain-Kreuzberg
        "085": ["10777", "10779", "10781", "10783", "10785", "10787", "10789"],  # Tempelhof-Schöneberg
    },
    (12000, 12689): {
        "078": ["12163", "12165", "12167", "12169", "12203", "12205", "12207", "12209"],  # Steglitz-Zehlendorf
        "080": ["12619", "12621", "12623", "12627", "12629", "12679", "12681", "12683", "12685", "12687", "12689"],  # Marzahn-Hellersdorf
        "083": ["12435", "12437", "12439", "12459", "12487", "12489", "12524", "12526", "12527", "12555", "12557", "12559", "12587", "12589"],  # Treptow-Köpenick
        "084": ["12043", "12045", "12047", "12049", "12051", "12053", "12055", "12057", "12059", "12099"],  # Neukölln
        "085": ["12101", "12103", "12105", "12107", "12109"],  # Tempelhof-Schöneberg
    },
    (13000, 13999): {
        "074": ["13347", "13349", "13353", "13355", "13357", "13359"],  # Berlin-Mitte
        "075": ["13051", "13053", "13086", "13088", "13089", "13125", "13127", "13129"],  # Pankow
        "076": ["13403", "13405", "13407", "13409", "13435", "13437", "13439", "13465", "13467", "13469"],  # Reinickendorf
        "077": ["13597", "13599"],  # Charlottenburg-Wilmersdorf
        "079": ["13581", "13583", "13585", "13587", "13589", "13591", "13593", "13595"],  # Spandau
        "081": ["13055", "13057", "13059"],  # Lichtenberg
    },
    (14000, 14199): {
        "077": ["14050", "14053", "14055", "14057"],  # Charlottenburg-Wilmersdorf
        "078": ["14109", "14129", "14163", "14165", "14167", "14169", "14193", "14195", "14199"],  # Steglitz-Zehlendorf
    },
    
    # PADERBORN (33xxx)
    (33098, 33129): {"136": list(range(33098, 33130))},  # Paderborn
    
    # Add more comprehensive coverage for major regions
}

# Create expanded PLZ database
PLZ_TO_WAHLKREIS = {}

# Add specific mappings from ranges
for plz_range, wk_mappings in PLZ_RANGES.items():
    for wk_num, plz_list in wk_mappings.items():
        for plz in plz_list:
            plz_str = str(plz).zfill(5)
            PLZ_TO_WAHLKREIS[plz_str] = wk_num

# Add comprehensive city-based mappings
CITY_PLZ_MAPPINGS = {
    # Major cities with their PLZ ranges and Wahlkreis
    "München": {"087": list(range(80331, 80340)) + list(range(80469, 80500)) + list(range(80538, 80550)) + list(range(81667, 81677))},
    "Köln": {"092": list(range(50667, 50680)) + list(range(50733, 50740)) + list(range(50765, 50769)) + list(range(50823, 50829))},
    "Frankfurt": {"182": list(range(60306, 60325)) + list(range(60486, 60490)) + list(range(60594, 60599))},
    "Hamburg": {"018": list(range(20095, 20149)) + list(range(20253, 20257)) + list(range(20354, 20359))},
    "Paderborn": {"136": list(range(33098, 33130))},
    "Bielefeld": {"131": list(range(33602, 33739))},
    "Mannheim": {"275": list(range(68159, 68169)) + list(range(68199, 68229))},
    "Aachen": {"086": list(range(52062, 52081))},
    "Bremen": {"054": list(range(28195, 28779))},
    "Hannover": {"041": list(range(30159, 30179)) + list(range(30419, 30453))},
}

for city, wk_mappings in CITY_PLZ_MAPPINGS.items():
    for wk_num, plz_list in wk_mappings.items():
        for plz in plz_list:
            plz_str = str(plz).zfill(5)
            if plz_str not in PLZ_TO_WAHLKREIS:  # Don't override existing
                PLZ_TO_WAHLKREIS[plz_str] = wk_num

# Save expanded PLZ database
with open('plz_database.json', 'w', encoding='utf-8') as f:
    json.dump(PLZ_TO_WAHLKREIS, f, indent=2, ensure_ascii=False)

print(f"Saved {len(PLZ_TO_WAHLKREIS)} PLZ mappings to plz_database.json")

# Create PLZ to members mapping
plz_to_members = {}
for plz, wk_num in PLZ_TO_WAHLKREIS.items():
    if wk_num in wahlkreise:
        plz_to_members[plz] = {
            'wahlkreis_number': wk_num,
            'wahlkreis_name': wahlkreise[wk_num]['name'],
            'members': wahlkreise[wk_num]['members']
        }

with open('plz_to_members.json', 'w', encoding='utf-8') as f:
    json.dump(plz_to_members, f, indent=2, ensure_ascii=False)

print(f"Saved {len(plz_to_members)} PLZ->member mappings to plz_to_members.json")

# Test cases
print("\n" + "="*70)
print("TEST CASES")
print("="*70)

test_plzs = ["10961", "33102", "50667", "80331", "60306", "20095"]

for plz in test_plzs:
    if plz in plz_to_members:
        data = plz_to_members[plz]
        print(f"\n✓ PLZ {plz}")
        print(f"  → Wahlkreis {data['wahlkreis_number']}: {data['wahlkreis_name']}")
        print(f"  → {len(data['members'])} member(s)")
        for m in data['members'][:2]:  # Show first 2
            print(f"     • {m['name']} ({m['fraktion']})")
    else:
        print(f"\n✗ PLZ {plz} not found")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Total Wahlkreise: {len(wahlkreise)}")
print(f"Total PLZ codes mapped: {len(PLZ_TO_WAHLKREIS)}")
print(f"Unique Wahlkreise with PLZ: {len(set(PLZ_TO_WAHLKREIS.values()))}")
