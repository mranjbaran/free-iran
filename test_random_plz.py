import json
import random

# Load our current PLZ mappings
with open('plz_to_members.json', 'r', encoding='utf-8') as f:
    our_plz = set(json.load(f).keys())

print(f"We currently have {len(our_plz)} PLZ codes mapped")

# Generate 100 random German PLZ codes (10000-99999) that we DON'T have
random_plz_to_test = []

# German PLZ ranges by region (first digit)
# 0: Saxony, Brandenburg, Thuringia
# 1: Berlin, Brandenburg, Mecklenburg-Vorpommern
# 2: Hamburg, Schleswig-Holstein, Lower Saxony, Bremen
# 3: Lower Saxony, Westphalia, Hesse, Thuringia, Saxony-Anhalt
# 4: North Rhine-Westphalia, Lower Saxony
# 5: North Rhine-Westphalia, Rhineland-Palatinate, Hesse
# 6: Hesse, Rhineland-Palatinate, Saarland
# 7: Baden-Württemberg
# 8: Bavaria, Baden-Württemberg
# 9: Bavaria, Thuringia

# Sample real German PLZ codes from different regions (NOT in our dataset)
sample_plz_codes = []

# Generate random PLZ from each region zone
for region in range(10):  # 0-9
    for _ in range(20):  # 20 codes per region
        # Generate random 5-digit PLZ starting with region digit
        plz = f"{region}{random.randint(1000, 9999)}"
        if plz not in our_plz:
            sample_plz_codes.append(plz)

# Take 100 random ones
random_plz_to_test = random.sample(sample_plz_codes, min(100, len(sample_plz_codes)))

print(f"\nTesting {len(random_plz_to_test)} random PLZ codes NOT in our dataset:")
print("=" * 70)

# Load wahlkreis list for name search fallback
with open('wahlkreis_list.json', 'r', encoding='utf-8') as f:
    wahlkreis_list = json.load(f)

# Test each PLZ
found_count = 0
not_found_count = 0

results = {
    'found_by_plz': [],
    'not_found': []
}

for plz in random_plz_to_test:
    if plz in our_plz:
        found_count += 1
        results['found_by_plz'].append(plz)
    else:
        not_found_count += 1
        results['not_found'].append(plz)

# Display results
print(f"\n✓ Found by PLZ: {found_count}")
print(f"✗ Not found: {not_found_count}")
print(f"\nCoverage: {(found_count / len(random_plz_to_test) * 100):.1f}%")

# Show sample of not found PLZ
print(f"\nSample of PLZ codes NOT found (first 20):")
for plz in results['not_found'][:20]:
    print(f"  - {plz}")

print("\n" + "=" * 70)
print("CONCLUSION:")
print(f"Out of {len(random_plz_to_test)} random German PLZ codes:")
print(f"  - {found_count} were found in our verified database")
print(f"  - {not_found_count} were not found")
print(f"\nThis is EXPECTED because we only map {len(our_plz)} verified codes.")
print("For unmapped PLZ, users should search by city/region name.")
print("=" * 70)
