import requests
import json

# Find Bundestag ID and explore the structure

print("=" * 80)
print("EXPLORING ABGEORDNETENWATCH.DE API STRUCTURE")
print("=" * 80)

# Step 1: Find Bundestag parliament
print("\n1. Finding Bundestag Parliament")
print("-" * 80)

parliaments_url = "https://www.abgeordnetenwatch.de/api/v2/parliaments"
response = requests.get(parliaments_url, timeout=10)
if response.status_code == 200:
    data = response.json()
    bundestag = None
    for parliament in data['data']:
        if 'bundestag' in parliament['label'].lower():
            bundestag = parliament
            print(f"Found: {parliament['label']} (ID: {parliament['id']})")
            print(json.dumps(parliament, indent=2, ensure_ascii=False))
            break
    
    if not bundestag:
        print("Bundestag not in first page, searching...")
        # Try direct ID 5 (mentioned in docs)
        bundestag_url = "https://www.abgeordnetenwatch.de/api/v2/parliaments/5"
        response = requests.get(bundestag_url, timeout=10)
        if response.status_code == 200:
            bundestag = response.json()['data']
            print(f"Found Bundestag by ID 5:")
            print(json.dumps(bundestag, indent=2, ensure_ascii=False))

# Step 2: Get current Bundestag period
print("\n\n2. Finding Current Bundestag Period")
print("-" * 80)

periods_url = "https://www.abgeordnetenwatch.de/api/v2/parliament-periods?parliament=5"
response = requests.get(periods_url, timeout=10)
if response.status_code == 200:
    data = response.json()
    print(f"Found {len(data['data'])} periods")
    # Get the most recent one
    current_period = data['data'][0]
    print(f"\nMost recent period:")
    print(json.dumps(current_period, indent=2, ensure_ascii=False)[:500])

# Step 3: Explore constituencies endpoint
print("\n\n3. Exploring Constituencies")
print("-" * 80)

constituencies_url = "https://www.abgeordnetenwatch.de/api/v2/constituencies?parliament=5&range_end=10"
response = requests.get(constituencies_url, timeout=10)
if response.status_code == 200:
    data = response.json()
    print(f"Found constituencies, showing first example:")
    if data['data']:
        constituency = data['data'][0]
        print(json.dumps(constituency, indent=2, ensure_ascii=False))

# Step 4: Check if constituencies have postal code field
print("\n\n4. Checking Constituency Fields")
print("-" * 80)

# Try getting a specific constituency
constituency_url = "https://www.abgeordnetenwatch.de/api/v2/constituencies/1"
response = requests.get(constituency_url, timeout=10)
if response.status_code == 200:
    constituency_data = response.json()
    print(f"Constituency structure:")
    print(json.dumps(constituency_data['data'], indent=2, ensure_ascii=False)[:1000])

# Step 5: Try candidacies-mandates endpoint (this links politicians to constituencies)
print("\n\n5. Exploring Candidacies-Mandates (Politicians in Constituencies)")
print("-" * 80)

mandates_url = "https://www.abgeordnetenwatch.de/api/v2/candidacies-mandates?parliament_period=111&range_end=5"
response = requests.get(mandates_url, timeout=10)
if response.status_code == 200:
    data = response.json()
    print(f"Found mandates, showing first example:")
    if data['data']:
        mandate = data['data'][0]
        print(json.dumps(mandate, indent=2, ensure_ascii=False)[:1000])

print("\n" + "=" * 80)
print("EXPLORATION COMPLETE")
print("=" * 80)
