import json

# Test PLZ codes provided by user
test_plz_codes = """01067
01277
04109
04179
06108
06132
10115
10245
10439
10587
10709
10997
13051
13507
14057
14467
14532
14776
15230
15517
17033
17489
18055
18109
19053
20095
20253
21073
22041
22761
23552
24103
24937
25813
26122
26603
26789
27568
28195
28359
28757
29221
30159
30449
30823
31224
32052
32423
33098
33602
34117
34497
35390
36037
37073
38100
38440
39104
39576
40213
40476
41061
42103
42651
44135
44787
45127
45879
46236
47051
47798
48143
49074
49477
50667
50825
51373
52062
53111
54290
55116
56068
57072
58095
59065
60311
60599
64283
65183
66111
68159
69117
70173
70565
72070
72764
73430
74072
80331
93047""".strip().split('\n')

# Load our PLZ database
with open('plz_to_members.json', 'r', encoding='utf-8') as f:
    plz_db = json.load(f)

# Load wahlkreis list
with open('wahlkreis_list.json', 'r', encoding='utf-8') as f:
    wahlkreis_list = json.load(f)

print("=" * 80)
print(f"TESTING {len(test_plz_codes)} SPECIFIC PLZ CODES")
print("=" * 80)

found = []
not_found = []

for plz in test_plz_codes:
    plz = plz.strip()
    if plz in plz_db:
        data = plz_db[plz]
        found.append({
            'plz': plz,
            'wahlkreis': data['wahlkreis_name'],
            'members': [m['name'] for m in data['members']]
        })
    else:
        not_found.append(plz)

print(f"\n✓ FOUND: {len(found)} PLZ codes")
print(f"✗ NOT FOUND: {len(not_found)} PLZ codes")
print(f"\nCoverage: {(len(found) / len(test_plz_codes) * 100):.1f}%")

print("\n" + "=" * 80)
print("FOUND PLZ CODES (Direct Match):")
print("=" * 80)
for item in found:
    print(f"\nPLZ {item['plz']} → {item['wahlkreis']}")
    for member in item['members']:
        print(f"  • {member}")

print("\n" + "=" * 80)
print(f"NOT FOUND PLZ CODES ({len(not_found)} codes):")
print("=" * 80)
for plz in not_found:
    print(f"  - {plz}")

print("\n" + "=" * 80)
print("RECOMMENDATION:")
print("=" * 80)
print(f"• {len(found)} PLZ codes can be found directly")
print(f"• {len(not_found)} PLZ codes require city/region name search")
print("\nFor missing PLZ codes, users should search by city name.")
print("=" * 80)
