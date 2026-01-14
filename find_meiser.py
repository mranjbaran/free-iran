import csv

# Find Meiser in the member list
with open('bundestag_complete.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    members = list(reader)

meiser_members = [m for m in members if 'Meiser' in m['name']]

print(f"Found {len(meiser_members)} members with 'Meiser' in name:\n")
for m in meiser_members:
    print(f"{m['name']:40} {m['fraktion']:25} mdbId: {m['mdbId']}")
