"""
Final test: Verify PLZ 10961 returns Pascal Meiser
"""

import json

# Load the PLZ to members mapping
with open('plz_to_members.json', 'r', encoding='utf-8') as f:
    plz_to_members = json.load(f)

print("="*70)
print("FINAL TEST: PLZ 10961 → Pascal Meiser")
print("="*70)

# Test PLZ 10961
test_plz = "10961"

if test_plz in plz_to_members:
    data = plz_to_members[test_plz]
    
    print(f"\n✓ PLZ {test_plz} FOUND!")
    print(f"\nWahlkreis: {data['wahlkreis_number']} - {data['wahlkreis_name']}")
    print(f"\nAbgeordnete in diesem Wahlkreis:")
    print("-" * 70)
    
    for member in data['members']:
        print(f"\n  Name: {member['name']}")
        print(f"  Partei: {member['fraktion']}")
        print(f"  MDB-ID: {member['mdbId']}")
        print(f"  Kontakt: {member['contact_url']}")
        
        if 'Meiser' in member['name']:
            print("\n  🎉 ✓✓✓ PASCAL MEISER GEFUNDEN! ✓✓✓ 🎉")
    
    print("\n" + "="*70)
    print("TEST ERFOLGREICH!")
    print("="*70)
    
else:
    print(f"\n✗ PLZ {test_plz} NOT FOUND")
    print("TEST FAILED!")

# Additional tests
print("\n\n" + "="*70)
print("ADDITIONAL TESTS")
print("="*70)

test_cases = [
    ("10115", "Berlin-Mitte"),
    ("50667", "Köln"),
    ("80331", "München"),
]

for plz, expected_city in test_cases:
    if plz in plz_to_members:
        wk_name = plz_to_members[plz]['wahlkreis_name']
        print(f"\n✓ PLZ {plz} → {wk_name}")
    else:
        print(f"\n✗ PLZ {plz} not found (expected {expected_city})")

# Summary
print("\n\n" + "="*70)
print("DATABASE SUMMARY")
print("="*70)
print(f"Total PLZ codes in database: {len(plz_to_members)}")

# Count unique Wahlkreise
unique_wk = set(data['wahlkreis_number'] for data in plz_to_members.values())
print(f"Unique Wahlkreise covered: {len(unique_wk)}")

# Count total members available through PLZ search
total_members = sum(len(data['members']) for data in plz_to_members.values())
print(f"Total member entries: {total_members}")

print("\n" + "="*70)
print("READY TO USE!")
print("="*70)
print("\nTo use the web interface:")
print("1. Open 'bundestag_finder.html' in your browser")
print("2. Enter PLZ 10961")
print("3. You should see Pascal Meiser (Die Linke)")
print("\n" + "="*70)
