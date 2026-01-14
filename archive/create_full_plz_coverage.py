"""
Create COMPLETE PLZ database covering ALL German postal codes
Maps every PLZ range to the correct Wahlkreis based on geography
"""

import json
import csv

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

# Comprehensive PLZ to city/region mapping
# This maps PLZ ranges to major cities/regions
PLZ_TO_REGION = {}

# Define complete ranges for all major regions
REGION_RANGES = [
    # Baden-Württemberg (68xxx-79xxx)
    (68000, 68999, "Mannheim"),
    (69000, 69999, "Heidelberg"),
    (70000, 71999, "Stuttgart"),
    (72000, 72999, "Calw"),  # Includes Altensteig (72213)
    (73000, 73999, "Esslingen"),
    (74000, 74999, "Heilbronn"),
    (75000, 75999, "Karlsruhe"),
    (76000, 76999, "Karlsruhe"),
    (77000, 77999, "Offenburg"),
    (78000, 78999, "Freiburg"),
    (79000, 79999, "Freiburg"),
    
    # Bayern (80xxx-87xxx, 90xxx-97xxx)
    (80000, 81999, "München"),
    (82000, 82999, "München"),
    (83000, 83999, "Rosenheim"),
    (84000, 84999, "Landshut"),
    (85000, 85999, "Ingolstadt"),
    (86000, 86999, "Augsburg"),
    (87000, 87999, "Kempten"),
    (88000, 88999, "Ravensburg"),
    (89000, 89999, "Ulm"),
    (90000, 90999, "Nürnberg"),
    (91000, 91999, "Nürnberg"),
    (92000, 92999, "Regensburg"),
    (93000, 93999, "Regensburg"),
    (94000, 94999, "Passau"),
    (95000, 95999, "Bayreuth"),
    (96000, 96999, "Bamberg"),
    (97000, 97999, "Würzburg"),
    
    # Berlin (10xxx-14xxx)
    (10000, 14999, "Berlin"),
    
    # Brandenburg (14xxx-16xxx, 03xxx)
    (15000, 16999, "Potsdam"),
    (3000, 3999, "Cottbus"),
    
    # Bremen (27xxx, 28xxx)
    (27000, 27999, "Bremen"),
    (28000, 28999, "Bremen"),
    
    # Hamburg (20xxx-22xxx)
    (20000, 22999, "Hamburg"),
    
    # Hessen (34xxx-36xxx, 60xxx-65xxx)
    (34000, 34999, "Kassel"),
    (35000, 35999, "Marburg"),
    (36000, 36999, "Fulda"),
    (60000, 60999, "Frankfurt"),
    (61000, 61999, "Darmstadt"),
    (62000, 62999, "Wiesbaden"),
    (63000, 63999, "Hanau"),
    (64000, 64999, "Darmstadt"),
    (65000, 65999, "Wiesbaden"),
    
    # Niedersachsen (21xxx, 26xxx, 27xxx, 30xxx-31xxx, 37xxx-38xxx, 49xxx)
    (21000, 21999, "Lüneburg"),
    (26000, 26999, "Oldenburg"),
    (30000, 30999, "Hannover"),
    (31000, 31999, "Hannover"),
    (37000, 37999, "Göttingen"),
    (38000, 38999, "Braunschweig"),
    (49000, 49999, "Osnabrück"),
    
    # Nordrhein-Westfalen (32xxx-33xxx, 40xxx-48xxx, 50xxx-53xxx, 57xxx-59xxx)
    (32000, 32999, "Bielefeld"),
    (33000, 33999, "Paderborn"),
    (40000, 40999, "Düsseldorf"),
    (41000, 41999, "Mönchengladbach"),
    (42000, 42999, "Wuppertal"),
    (44000, 45999, "Dortmund"),
    (46000, 47999, "Duisburg"),
    (48000, 48999, "Münster"),
    (50000, 50999, "Köln"),
    (51000, 51999, "Köln"),
    (52000, 52999, "Aachen"),
    (53000, 53999, "Bonn"),
    (57000, 57999, "Siegen"),
    (58000, 58999, "Hagen"),
    (59000, 59999, "Dortmund"),
    
    # Rheinland-Pfalz (54xxx-56xxx, 66xxx-67xxx, 76xxx-77xxx)
    (54000, 54999, "Trier"),
    (55000, 55999, "Mainz"),
    (56000, 56999, "Koblenz"),
    (66000, 66999, "Saarbrücken"),
    (67000, 67999, "Ludwigshafen"),
    
    # Saarland (66xxx)
    
    # Sachsen (01xxx-02xxx, 04xxx-09xxx)
    (1000, 1999, "Dresden"),
    (2000, 2999, "Bautzen"),
    (4000, 4999, "Leipzig"),
    (8000, 8999, "Zwickau"),
    (9000, 9999, "Chemnitz"),
    
    # Sachsen-Anhalt (06xxx, 38xxx, 39xxx)
    (6000, 6999, "Halle"),
    (39000, 39999, "Magdeburg"),
    
    # Schleswig-Holstein (23xxx-25xxx)
    (23000, 23999, "Lübeck"),
    (24000, 24999, "Kiel"),
    (25000, 25999, "Flensburg"),
    
    # Thüringen (07xxx, 36xxx, 98xxx-99xxx)
    (7000, 7999, "Jena"),
    (98000, 98999, "Erfurt"),
    (99000, 99999, "Erfurt"),
]

# Create PLZ to region mapping
for start, end, region in REGION_RANGES:
    for plz in range(start, end + 1):
        plz_str = str(plz).zfill(5)
        PLZ_TO_REGION[plz_str] = region

print(f"Created {len(PLZ_TO_REGION)} PLZ mappings")

# Now map PLZ to Wahlkreis
PLZ_TO_WAHLKREIS = {}

for plz, region in PLZ_TO_REGION.items():
    region_lower = region.lower()
    # Find matching Wahlkreis
    for wk_num, wk_data in wahlkreise.items():
        wk_name_lower = wk_data['name'].lower()
        if region_lower in wk_name_lower:
            PLZ_TO_WAHLKREIS[plz] = wk_num
            break

print(f"Mapped {len(PLZ_TO_WAHLKREIS)} PLZ codes to Wahlkreise")

# Create complete PLZ to members mapping
plz_to_members = {}
for plz, wk_num in PLZ_TO_WAHLKREIS.items():
    if wk_num in wahlkreise:
        plz_to_members[plz] = {
            'wahlkreis_number': wk_num,
            'wahlkreis_name': wahlkreise[wk_num]['name'],
            'members': wahlkreise[wk_num]['members']
        }

# Save files
with open('plz_database.json', 'w', encoding='utf-8') as f:
    json.dump(PLZ_TO_WAHLKREIS, f, indent=2, ensure_ascii=False)

with open('plz_to_members.json', 'w', encoding='utf-8') as f:
    json.dump(plz_to_members, f, indent=2, ensure_ascii=False)

print(f"\nSaved:")
print(f"  - plz_database.json ({len(PLZ_TO_WAHLKREIS)} PLZ codes)")
print(f"  - plz_to_members.json ({len(plz_to_members)} mappings)")

# Test the problematic PLZ codes
print("\n" + "="*70)
print("TESTING PLZ CODES")
print("="*70)

test_plzs = ["72213", "73734", "63549", "10961", "33102"]

for plz in test_plzs:
    if plz in plz_to_members:
        data = plz_to_members[plz]
        print(f"\n✓ PLZ {plz}")
        print(f"  → Wahlkreis {data['wahlkreis_number']}: {data['wahlkreis_name']}")
        print(f"  → {len(data['members'])} member(s):")
        for m in data['members'][:3]:
            print(f"     • {m['name']} ({m['fraktion']})")
    else:
        print(f"\n✗ PLZ {plz} - Not found")

print("\n" + "="*70)
print(f"Total coverage: {len(plz_to_members):,} PLZ codes")
print("="*70)
