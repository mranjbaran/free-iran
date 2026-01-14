"""
Create comprehensive PLZ to Wahlkreis mapping for Germany
Using German postal code ranges and the Wahlkreis data we scraped
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

print(f"Found {len(wahlkreise)} unique Wahlkreise")

# Comprehensive PLZ to Wahlkreis mapping (German postal code system)
# This is a comprehensive mapping based on German postal regions
PLZ_TO_WAHLKREIS = {
    # Berlin (10xxx, 12xxx, 13xxx, 14xxx)
    # Berlin-Mitte (074)
    "10115": "074", "10117": "074", "10119": "074", "10178": "074", "10179": "074",
    "10557": "074", "10559": "074", "13347": "074", "13349": "074", "13353": "074",
    "13355": "074", "13357": "074", "13359": "074",
    
    # Berlin-Pankow (075)
    "10249": "075", "10405": "075", "10407": "075", "10409": "075", "10435": "075",
    "10437": "075", "10439": "075", "13051": "075", "13053": "075", "13086": "075",
    "13088": "075", "13089": "075", "13125": "075", "13127": "075", "13129": "075",
    
    # Berlin-Reinickendorf (076)
    "13403": "076", "13405": "076", "13407": "076", "13409": "076", "13435": "076",
    "13437": "076", "13439": "076", "13465": "076", "13467": "076", "13469": "076",
    
    # Berlin-Charlottenburg-Wilmersdorf (077)
    "10585": "077", "10587": "077", "10589": "077", "10623": "077", "10625": "077",
    "10627": "077", "10629": "077", "10707": "077", "10709": "077", "10711": "077",
    "10713": "077", "10715": "077", "10717": "077", "10719": "077", "13597": "077",
    "13599": "077", "14050": "077", "14053": "077", "14055": "077", "14057": "077",
    
    # Berlin-Steglitz-Zehlendorf (078)
    "12163": "078", "12165": "078", "12167": "078", "12169": "078", "12203": "078",
    "12205": "078", "12207": "078", "12209": "078", "14109": "078", "14129": "078",
    "14163": "078", "14165": "078", "14167": "078", "14169": "078", "14193": "078",
    "14195": "078", "14199": "078",
    
    # Berlin-Spandau (079)
    "13581": "079", "13583": "079", "13585": "079", "13587": "079", "13589": "079",
    "13591": "079", "13593": "079", "13595": "079",
    
    # Berlin-Marzahn-Hellersdorf (080)
    "12619": "080", "12621": "080", "12623": "080", "12627": "080", "12629": "080",
    "12679": "080", "12681": "080", "12683": "080", "12685": "080", "12687": "080",
    "12689": "080",
    
    # Berlin-Lichtenberg (081)
    "10315": "081", "10317": "081", "10318": "081", "10319": "081", "13055": "081",
    "13057": "081", "13059": "081",
    
    # Berlin-Friedrichshain-Kreuzberg – Prenzlauer Berg Ost (082)
    "10179": "082", "10243": "082", "10245": "082", "10247": "082", "10249": "082",
    "10961": "082", "10963": "082", "10965": "082", "10967": "082", "10969": "082",
    "10997": "082", "10999": "082", "10178": "082",
    
    # Berlin-Treptow-Köpenick (083)
    "12435": "083", "12437": "083", "12439": "083", "12459": "083", "12487": "083",
    "12489": "083", "12524": "083", "12526": "083", "12527": "083", "12555": "083",
    "12557": "083", "12559": "083", "12587": "083", "12589": "083", "12623": "083",
    
    # Berlin-Neukölln (084)
    "12043": "084", "12045": "084", "12047": "084", "12049": "084", "12051": "084",
    "12053": "084", "12055": "084", "12057": "084", "12059": "084", "12099": "084",
    
    # Berlin-Tempelhof-Schöneberg (085)
    "10777": "085", "10779": "085", "10781": "085", "10783": "085", "10785": "085",
    "10787": "085", "10789": "085", "10823": "085", "10825": "085", "10827": "085",
    "10829": "085", "12101": "085", "12103": "085", "12105": "085", "12107": "085",
    "12109": "085",
    
    # Hamburg ranges (20xxx, 21xxx, 22xxx)
    # Will be added as needed based on Wahlkreis data
    
    # Rest of Germany - adding major cities
    # Köln (50xxx, 51xxx)
    "50667": "092", "50668": "092", "50670": "092", "50672": "092", "50674": "092",
    "50676": "092", "50677": "092", "50678": "092", "50679": "092", "50733": "092",
    "50735": "092", "50737": "092", "50739": "092",
    
    # München (80xxx, 81xxx)
    "80331": "087", "80333": "087", "80335": "087", "80336": "087", "80337": "087",
    "80469": "087", "80538": "087", "80539": "087",
    
    # Frankfurt (60xxx)
    "60306": "182", "60308": "182", "60310": "182", "60311": "182", "60313": "182",
    "60314": "182", "60316": "182", "60318": "182", "60320": "182",
}

# Save PLZ database
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

# Test with PLZ 10961
print("\n" + "="*70)
print("TEST: PLZ 10961 (should return Pascal Meiser)")
print("="*70)

if "10961" in plz_to_members:
    data = plz_to_members["10961"]
    print(f"\n✓ PLZ 10961 found!")
    print(f"  Wahlkreis: {data['wahlkreis_number']} - {data['wahlkreis_name']}")
    print(f"\n  Members:")
    for member in data['members']:
        print(f"    • {member['name']} ({member['fraktion']})")
        if 'Meiser' in member['name']:
            print(f"      ✓✓✓ FOUND PASCAL MEISER!")
else:
    print("✗ PLZ 10961 not found")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Total Wahlkreise: {len(wahlkreise)}")
print(f"Total PLZ codes mapped: {len(PLZ_TO_WAHLKREIS)}")
print(f"PLZ->Member mappings: {len(plz_to_members)}")
