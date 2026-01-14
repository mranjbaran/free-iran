import json

data = json.load(open('plz_to_members.json', encoding='utf-8'))

print('Testing PLZ 73734:', '73734' in data)
print('Testing PLZ 63549:', '63549' in data)
print()

if '73734' in data:
    print('73734 ->', data['73734']['wahlkreis_name'])
    print('  Members:', [m['name'] for m in data['73734']['members']])
    print()

if '63549' in data:
    print('63549 ->', data['63549']['wahlkreis_name'])
    print('  Members:', [m['name'] for m in data['63549']['members']])
