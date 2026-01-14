import json
import csv

# Berlin PLZ to Wahlkreis mapping (Berlin has specific districts)
# PLZ 10961 is in Berlin-Kreuzberg, which is part of Wahlkreis 083 (Berlin-Friedrichshain-Kreuzberg – Prenzlauer Berg Ost)
# But looking at our data, we need to find which Berlin Wahlkreis we have

# Let's create a comprehensive PLZ database for Germany
# This is a sample - in production you'd use a complete PLZ database

BERLIN_PLZ_MAPPING = {
    # Berlin-Mitte (WK 074)
    "10115": 74, "10117": 74, "10119": 74, "10178": 74, "10179": 74,
    "10435": 74, "10557": 74, "10559": 74,
    
    # Berlin-Friedrichshain-Kreuzberg (WK 083)
    "10243": 83, "10245": 83, "10247": 83, "10249": 83,
    "10961": 83, "10963": 83, "10965": 83, "10967": 83, "10969": 83,
    "10997": 83, "10999": 83,
    
    # Berlin-Pankow (WK 075)
    "10405": 75, "10407": 75, "10409": 75, "10435": 75, "10437": 75,
    "10439": 75, "13051": 75, "13053": 75, "13055": 75, "13057": 75,
    "13086": 75, "13088": 75, "13089": 75,
    
    # Berlin-Steglitz-Zehlendorf (WK 078)
    "12163": 78, "12165": 78, "12167": 78, "12169": 78,
    "12203": 78, "12205": 78, "12207": 78, "12209": 78,
    "14109": 78, "14129": 78, "14163": 78, "14165": 78, "14167": 78, "14169": 78,
    "14193": 78, "14195": 78, "14199": 78,
}

# Sample PLZ mappings for other cities we have in our data
PLZ_TO_WAHLKREIS = {
    # Osnabrück (WK 039)
    **{str(plz): 39 for plz in range(49074, 49090)},
    
    # Aachen (WK 086)
    **{str(plz): 86 for plz in range(52062, 52081)},
    
    # Bamberg (WK 235)
    **{str(plz): 235 for plz in range(96047, 96054)},
    
    # Bielefeld (WK 131)
    **{str(plz): 131 for plz in range(33602, 33739)},
    
    # Berlin - add all Berlin mappings
    **{str(plz): wk for plz, wk in BERLIN_PLZ_MAPPING.items()},
}

def find_members_by_plz(plz, members_file='members_with_wahlkreis.csv'):
    """
    Find Bundestag members by PLZ
    """
    
    # Check if PLZ is in our mapping
    plz_str = str(plz)
    
    # Try exact match first
    if plz_str in PLZ_TO_WAHLKREIS:
        wahlkreis_num = PLZ_TO_WAHLKREIS[plz_str]
    else:
        # Try prefix match (first 3 digits)
        prefix = plz_str[:3]
        matches = [wk for p, wk in PLZ_TO_WAHLKREIS.items() if p.startswith(prefix)]
        if matches:
            wahlkreis_num = matches[0]
        else:
            print(f"PLZ {plz} not found in database")
            return []
    
    print(f"PLZ {plz} → Wahlkreis {wahlkreis_num}")
    
    # Load members and filter by Wahlkreis
    members = []
    with open(members_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['wahlkreis_number'] == str(wahlkreis_num):
                members.append(row)
    
    return members


def test_plz_search():
    """
    Test the PLZ search functionality
    """
    
    test_cases = [
        ("10961", "Pascal Meiser, Die Linke"),  # Berlin-Kreuzberg
        ("52062", "Lukas Benner or Armin Laschet"),  # Aachen
        ("49074", "Mathias Middelberg"),  # Osnabrück
        ("96047", "Thomas Silberhorn"),  # Bamberg
    ]
    
    print("="*70)
    print("TESTING PLZ SEARCH")
    print("="*70)
    
    for plz, expected in test_cases:
        print(f"\n{'='*70}")
        print(f"PLZ: {plz}")
        print(f"Expected: {expected}")
        print(f"{'='*70}")
        
        members = find_members_by_plz(plz)
        
        if members:
            print(f"✓ Found {len(members)} member(s):")
            for m in members:
                print(f"  • {m['name']} ({m['fraktion']})")
                print(f"    Wahlkreis: {m['wahlkreis_number']} - {m['wahlkreis_name']}")
                print(f"    Contact: {m['contact_url']}")
        else:
            print(f"✗ No members found")


if __name__ == "__main__":
    test_plz_search()
    
    print("\n\n" + "="*70)
    print("INTERACTIVE TEST")
    print("="*70)
    print("\nEnter a PLZ to search (or 'quit' to exit):")
    
    while True:
        plz = input("\nPLZ: ").strip()
        
        if plz.lower() in ['quit', 'exit', 'q']:
            break
        
        if not plz.isdigit() or len(plz) != 5:
            print("Invalid PLZ. Please enter a 5-digit postal code.")
            continue
        
        members = find_members_by_plz(plz)
        
        if members:
            print(f"\n✓ Found {len(members)} member(s) for PLZ {plz}:")
            for m in members:
                print(f"\n  {m['name']}")
                print(f"  Party: {m['fraktion']}")
                print(f"  Wahlkreis: {m['wahlkreis_number']} - {m['wahlkreis_name']}")
                print(f"  Contact: {m['contact_url']}")
        else:
            print(f"\n✗ No members found for PLZ {plz}")
            print("This PLZ might not be in our database yet.")
