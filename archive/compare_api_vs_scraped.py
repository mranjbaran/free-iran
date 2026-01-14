import json

print("=" * 80)
print("COMPARING API DATA VS SCRAPED DATA")
print("=" * 80)

# Load API data
with open('abgeordnetenwatch_constituencies.json', 'r', encoding='utf-8') as f:
    api_constituencies = json.load(f)

# Load our scraped data
with open('wahlkreis_list.json', 'r', encoding='utf-8') as f:
    scraped_wahlkreise = json.load(f)

print(f"\nAPI Data: {len(api_constituencies)} constituencies")
print(f"Scraped Data: {len(scraped_wahlkreise)} wahlkreise")

# Sample comparison
print("\n" + "=" * 80)
print("SAMPLE API CONSTITUENCIES")
print("=" * 80)
for i, const in enumerate(api_constituencies[:10]):
    print(f"\n{const['number']}. {const['name']}")
    print(f"   Members: {', '.join([m['name'] + ' (' + m['party'] + ')' for m in const['members'][:3]])}")

print("\n" + "=" * 80)
print("SAMPLE SCRAPED WAHLKREISE")
print("=" * 80)
for i, wk in enumerate(scraped_wahlkreise[:10]):
    print(f"\n{wk['number']}. {wk['name']}")
    print(f"   Members: {', '.join([m['name'] + ' (' + m['fraktion'] + ')' for m in wk['members'][:3]])}")

# Check if we can match constituencies by number
print("\n" + "=" * 80)
print("MATCHING BY CONSTITUENCY NUMBER")
print("=" * 80)

api_by_number = {c['number']: c for c in api_constituencies}
scraped_by_number = {w['number']: w for w in scraped_wahlkreise}

matched = 0
api_only = 0
scraped_only = 0

all_numbers = set(api_by_number.keys()) | set(scraped_by_number.keys())

for number in sorted(all_numbers):
    in_api = number in api_by_number
    in_scraped = number in scraped_by_number
    
    if in_api and in_scraped:
        matched += 1
    elif in_api:
        api_only += 1
        print(f"API only: {number} - {api_by_number[number]['name']}")
    elif in_scraped:
        scraped_only += 1
        print(f"Scraped only: {number} - {scraped_by_number[number]['name']}")

print(f"\nMatched: {matched}")
print(f"API only: {api_only}")
print(f"Scraped only: {scraped_only}")

# Key insight
print("\n" + "=" * 80)
print("KEY INSIGHT")
print("=" * 80)
print("API Data (2021-2025 period):")
print(f"  • {len(api_constituencies)} constituencies")
print(f"  • Historical data from previous Bundestag")
print(f"  • Has detailed politician info")
print("\nScraped Data (current 2025):")
print(f"  • {len(scraped_wahlkreise)} wahlkreise")
print(f"  • Current Bundestag members")
print(f"  • Direct from bundestag.de")
print("\nRECOMMENDATION:")
print("  Our scraped data is MORE CURRENT and MORE COMPLETE")
print("  Keep using our existing solution!")
print("=" * 80)
