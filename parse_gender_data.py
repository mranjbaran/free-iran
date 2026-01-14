"""
Parse german_names_gender.md and create a gender lookup dictionary
"""
import re

# Read the markdown file
with open(r'C:\Users\sranjbar\Downloads\german_names_gender.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the table (skip header rows)
lines = content.split('\n')
gender_map = {}

for line in lines[3:]:  # Skip header and separator
    if '|' not in line or not line.strip():
        continue
    
    parts = [p.strip() for p in line.split('|')]
    if len(parts) >= 4:
        full_name = parts[1]
        first_name = parts[2]
        gender = parts[3]
        
        if full_name and gender and full_name != 'Full Name':
            # Store both "Last, First" and "First Last" formats
            gender_lower = gender.lower()
            
            # Original format from CSV
            gender_map[full_name.lower()] = gender_lower
            
            # Reverse format (First Last)
            if ', ' in full_name:
                name_parts = full_name.split(', ', 1)
                reversed_name = f"{name_parts[1]} {name_parts[0]}"
                gender_map[reversed_name.lower()] = gender_lower

print(f"Parsed {len(gender_map)} gender mappings")

# Write to a Python file
with open('gender_data.py', 'w', encoding='utf-8') as f:
    f.write('# Auto-generated gender lookup from german_names_gender.md\n')
    f.write('# Maps full MP names to gender\n\n')
    f.write('GENDER_LOOKUP = {\n')
    for name, gender in sorted(gender_map.items()):
        f.write(f'    {repr(name)}: {repr(gender)},\n')
    f.write('}\n')

# Count by gender
male_count = sum(1 for g in gender_map.values() if g == 'male')
female_count = sum(1 for g in gender_map.values() if g == 'female')
unknown_count = sum(1 for g in gender_map.values() if g == 'unknown')

print(f"\nStatistics:")
print(f"Male: {male_count}")
print(f"Female: {female_count}")
print(f"Unknown: {unknown_count}")
print(f"\nGenerated gender_data.py successfully!")
