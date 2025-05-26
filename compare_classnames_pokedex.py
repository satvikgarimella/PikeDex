import json

CLASS_FILE = "class_names.txt"
POKEDEX_FILE = "backend/pokedex_data.json"

with open(CLASS_FILE, "r") as f:
    class_names = set(line.strip() for line in f if line.strip())

with open(POKEDEX_FILE, "r") as f:
    pokedex_names = set(json.load(f).keys())

missing_in_pokedex = class_names - pokedex_names
missing_in_classnames = pokedex_names - class_names

if missing_in_pokedex:
    print(f"Names in class_names.txt but NOT in pokedex_data.json ({len(missing_in_pokedex)}):")
    for name in sorted(missing_in_pokedex):
        print(f"  {name}")
else:
    print("✅ All class_names.txt entries are present in pokedex_data.json.")

if missing_in_classnames:
    print(f"\nNames in pokedex_data.json but NOT in class_names.txt ({len(missing_in_classnames)}):")
    for name in sorted(missing_in_classnames):
        print(f"  {name}")
else:
    print("✅ All pokedex_data.json entries are present in class_names.txt.") 