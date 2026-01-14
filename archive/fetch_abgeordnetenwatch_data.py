import requests
import json
import time

print("=" * 80)
print("FETCHING ALL CURRENT BUNDESTAG MEMBERS FROM API")
print("=" * 80)

# Try period 132 (Bundestag 2021-2025) - more complete data
parliament_period = 132

# Get all mandates for current Bundestag
print(f"\nFetching all mandates for period {parliament_period}...")

all_mandates = []
page = 0
pager_limit = 100

while True:
    url = f"https://www.abgeordnetenwatch.de/api/v2/candidacies-mandates?parliament_period={parliament_period}&type=mandate&page={page}&pager_limit={pager_limit}"
    print(f"Fetching page {page}...")
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            
            if not data['data']:
                print("No more data")
                break
            
            all_mandates.extend(data['data'])
            print(f"  Got {len(data['data'])} mandates (total: {len(all_mandates)})")
            
            # Check if there are more pages
            meta = data.get('meta', {})
            result = meta.get('result', {})
            total = result.get('total', 0)
            count = result.get('count', 0)
            
            print(f"  API reports: {count} on this page, {total} total")
            
            if len(all_mandates) >= total:
                break
            
            page += 1
            time.sleep(0.5)  # Be nice to the API
        else:
            print(f"Error: {response.status_code}")
            print(response.text[:200])
            break
    except Exception as e:
        print(f"Exception: {e}")
        break

print(f"\n✓ Fetched {len(all_mandates)} total mandates")

# Process and show sample
print("\n" + "=" * 80)
print("SAMPLE MANDATES")
print("=" * 80)

for i, mandate in enumerate(all_mandates[:5]):
    politician = mandate.get('politician', {})
    electoral_data = mandate.get('electoral_data', {})
    constituency = electoral_data.get('constituency', {}) if electoral_data else {}
    fraction = mandate.get('fraction_membership', [])
    
    print(f"\n{i+1}. {politician.get('label', 'Unknown')}")
    print(f"   Constituency: {constituency.get('label', 'N/A')}")
    print(f"   Constituency ID: {constituency.get('id', 'N/A')}")
    if fraction:
        print(f"   Fraction: {fraction[0].get('label', 'N/A') if isinstance(fraction, list) else 'N/A'}")

# Save to file for analysis
output_file = 'abgeordnetenwatch_mandates.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_mandates, f, indent=2, ensure_ascii=False)

print(f"\n✓ Saved all mandates to {output_file}")

# Analyze unique constituencies
constituencies = {}
for mandate in all_mandates:
    electoral_data = mandate.get('electoral_data', {})
    const = electoral_data.get('constituency') if electoral_data else None
    
    if const and const.get('id'):
        const_id = const['id']
        const_label = const.get('label', 'Unknown')
        
        # Extract constituency number and name from label (format: "205 - Mainz (Bundestag 2021 - 2025)")
        parts = const_label.split(' - ')
        const_number = parts[0].strip() if len(parts) > 0 else 'N/A'
        const_name = parts[1].split('(')[0].strip() if len(parts) > 1 else 'Unknown'
        
        if const_id not in constituencies:
            constituencies[const_id] = {
                'id': const_id,
                'number': const_number,
                'name': const_name,
                'label': const_label,
                'members': []
            }
        
        politician = mandate.get('politician', {})
        fraction = mandate.get('fraction_membership', [])
        party = fraction[0].get('fraction', {}).get('label', 'Unknown') if fraction else 'Unknown'
        # Simplify party name (remove period info)
        party = party.split('(')[0].strip()
        
        constituencies[const_id]['members'].append({
            'name': politician.get('label', 'Unknown'),
            'id': politician.get('id'),
            'party': party
        })

print(f"\n✓ Found {len(constituencies)} unique constituencies")

# Save constituencies mapping
constituencies_file = 'abgeordnetenwatch_constituencies.json'
with open(constituencies_file, 'w', encoding='utf-8') as f:
    json.dump(list(constituencies.values()), f, indent=2, ensure_ascii=False)

print(f"✓ Saved constituencies to {constituencies_file}")

print("\n" + "=" * 80)
print(f"SUMMARY: {len(all_mandates)} mandates, {len(constituencies)} constituencies")
print("=" * 80)
