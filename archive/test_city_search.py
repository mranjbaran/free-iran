import json

# Common knowledge: German major city PLZ ranges
city_mapping = {
    "01067": "Dresden",
    "01277": "Dresden", 
    "04109": "Leipzig",
    "04179": "Leipzig",
    "06108": "Halle",
    "06132": "Halle",
    "10115": "Berlin",
    "10245": "Berlin",
    "10439": "Berlin",
    "10587": "Berlin",
    "10709": "Berlin",
    "10997": "Berlin",
    "13051": "Berlin",
    "13507": "Berlin",
    "14057": "Berlin",
    "14467": "Potsdam",
    "14532": "Kleinmachnow",
    "14776": "Brandenburg",
    "15230": "Frankfurt (Oder)",
    "15517": "Fürstenwalde",
    "17033": "Neubrandenburg",
    "17489": "Greifswald",
    "18055": "Rostock",
    "18109": "Rostock",
    "19053": "Schwerin",
    "20095": "Hamburg",
    "20253": "Hamburg",
    "21073": "Hamburg",
    "22041": "Hamburg",
    "22761": "Hamburg",
    "23552": "Lübeck",
    "24103": "Kiel",
    "24937": "Flensburg",
    "25813": "Husum",
    "26122": "Oldenburg",
    "26603": "Aurich",
    "26789": "Leer",
    "27568": "Bremerhaven",
    "28195": "Bremen",
    "28359": "Bremen",
    "28757": "Bremen",
    "29221": "Celle",
    "30159": "Hannover",
    "30449": "Hannover",
    "30823": "Garbsen",
    "31224": "Peine",
    "32052": "Herford",
    "32423": "Minden",
    "33098": "Paderborn",
    "33602": "Bielefeld",
    "34117": "Kassel",
    "34497": "Korbach",
    "35390": "Gießen",
    "36037": "Fulda",
    "37073": "Göttingen",
    "38100": "Braunschweig",
    "38440": "Wolfsburg",
    "39104": "Magdeburg",
    "39576": "Stendal",
    "40213": "Düsseldorf",
    "40476": "Düsseldorf",
    "41061": "Mönchengladbach",
    "42103": "Wuppertal",
    "42651": "Solingen",
    "44135": "Dortmund",
    "44787": "Bochum",
    "45127": "Essen",
    "45879": "Gelsenkirchen",
    "46236": "Bottrop",
    "47051": "Duisburg",
    "47798": "Krefeld",
    "48143": "Münster",
    "49074": "Osnabrück",
    "49477": "Ibbenbüren",
    "50667": "Köln",
    "50825": "Köln",
    "51373": "Leverkusen",
    "52062": "Aachen",
    "53111": "Bonn",
    "54290": "Trier",
    "55116": "Mainz",
    "56068": "Koblenz",
    "57072": "Siegen",
    "58095": "Hagen",
    "59065": "Hamm",
    "60311": "Frankfurt",
    "60599": "Frankfurt",
    "64283": "Darmstadt",
    "65183": "Wiesbaden",
    "66111": "Saarbrücken",
    "68159": "Mannheim",
    "69117": "Heidelberg",
    "70173": "Stuttgart",
    "70565": "Stuttgart",
    "72070": "Tübingen",
    "72764": "Reutlingen",
    "73430": "Aalen",
    "74072": "Heilbronn",
    "80331": "München",
    "93047": "Regensburg"
}

# Load wahlkreis list
with open('wahlkreis_list.json', 'r', encoding='utf-8') as f:
    wahlkreis_list = json.load(f)

# Load PLZ database
with open('plz_to_members.json', 'r', encoding='utf-8') as f:
    plz_db = json.load(f)

print("=" * 80)
print("TESTING CITY NAME SEARCH FOR UNMAPPED PLZ CODES")
print("=" * 80)

found_by_plz = 0
found_by_city = 0
not_found = 0

results = []

for plz, city in city_mapping.items():
    # Check if PLZ is in database
    if plz in plz_db:
        found_by_plz += 1
        results.append({
            'plz': plz,
            'city': city,
            'status': 'FOUND_BY_PLZ',
            'wahlkreis': plz_db[plz]['wahlkreis_name']
        })
    else:
        # Check if city name search would work
        city_lower = city.lower()
        matching_wahlkreise = []
        
        for wk in wahlkreis_list:
            if city_lower in wk['name'].lower():
                matching_wahlkreise.append(wk['name'])
        
        if matching_wahlkreise:
            found_by_city += 1
            results.append({
                'plz': plz,
                'city': city,
                'status': 'FOUND_BY_CITY',
                'wahlkreise': matching_wahlkreise
            })
        else:
            not_found += 1
            results.append({
                'plz': plz,
                'city': city,
                'status': 'NOT_FOUND'
            })

print(f"\n✓ Found by PLZ: {found_by_plz}")
print(f"✓ Found by City Name: {found_by_city}")
print(f"✗ Not Found: {not_found}")
print(f"\nTotal Coverage: {((found_by_plz + found_by_city) / len(city_mapping) * 100):.1f}%")

# Show examples of each category
print("\n" + "=" * 80)
print("SAMPLE: FOUND BY PLZ (Direct Match)")
print("=" * 80)
for item in [r for r in results if r['status'] == 'FOUND_BY_PLZ'][:5]:
    print(f"PLZ {item['plz']} ({item['city']}) → {item['wahlkreis']}")

print("\n" + "=" * 80)
print("SAMPLE: FOUND BY CITY NAME SEARCH")
print("=" * 80)
for item in [r for r in results if r['status'] == 'FOUND_BY_CITY'][:10]:
    print(f"PLZ {item['plz']} ({item['city']}) → Search '{item['city']}' finds:")
    for wk in item['wahlkreise'][:3]:
        print(f"  • {wk}")

print("\n" + "=" * 80)
print("NOT FOUND (Neither PLZ nor City Search)")
print("=" * 80)
not_found_items = [r for r in results if r['status'] == 'NOT_FOUND']
if not_found_items:
    for item in not_found_items:
        print(f"PLZ {item['plz']} ({item['city']})")
else:
    print("✓ All PLZ codes can be found either by PLZ or city name!")

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)
print(f"Out of {len(city_mapping)} major city PLZ codes:")
print(f"  • {found_by_plz} found by direct PLZ lookup")
print(f"  • {found_by_city} found by city name search")
print(f"  • {not_found} not found by either method")
print(f"\nTotal coverage: {((found_by_plz + found_by_city) / len(city_mapping) * 100):.1f}%")
print("=" * 80)
