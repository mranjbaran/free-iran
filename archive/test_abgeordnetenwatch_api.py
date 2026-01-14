import requests
import json

# Test the abgeordnetenwatch.de API

print("=" * 80)
print("TESTING ABGEORDNETENWATCH.DE API")
print("=" * 80)

# Test 1: Get constituency by PLZ
test_plz_codes = ["10115", "80331", "38678", "72213", "33098"]

print("\n1. Testing PLZ → Constituency mapping")
print("-" * 80)

for plz in test_plz_codes:
    url = f"https://www.abgeordnetenwatch.de/api/v2/constituencies?postal_code={plz}"
    print(f"\nTesting PLZ: {plz}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {data.keys()}")
            print(f"Data sample: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")
        else:
            print(f"Error: {response.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")

# Test 2: Try to get politicians endpoint structure
print("\n\n2. Testing Politicians endpoint structure")
print("-" * 80)

politicians_url = "https://www.abgeordnetenwatch.de/api/v2/politicians?range_end=5"
print(f"URL: {politicians_url}")

try:
    response = requests.get(politicians_url, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {data.keys()}")
        if 'data' in data and len(data['data']) > 0:
            print(f"\nSample politician structure:")
            print(json.dumps(data['data'][0], indent=2, ensure_ascii=False)[:1000])
    else:
        print(f"Error: {response.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")

# Test 3: Get Bundestag parliament ID
print("\n\n3. Testing Parliaments endpoint")
print("-" * 80)

parliaments_url = "https://www.abgeordnetenwatch.de/api/v2/parliaments"
print(f"URL: {parliaments_url}")

try:
    response = requests.get(parliaments_url, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {data.keys()}")
        if 'data' in data:
            print(f"\nAvailable parliaments:")
            for parliament in data['data'][:10]:
                print(f"  - ID: {parliament.get('id')}, Name: {parliament.get('label')}")
    else:
        print(f"Error: {response.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "=" * 80)
print("API TEST COMPLETE")
print("=" * 80)
