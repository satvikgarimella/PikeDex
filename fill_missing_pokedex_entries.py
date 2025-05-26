import json

CLASS_FILE = "class_names.txt"
POKEDEX_FILE = "backend/pokedex_data.json"

with open(CLASS_FILE, "r") as f:
    class_names = [line.strip() for line in f if line.strip()]

with open(POKEDEX_FILE, "r") as f:
    pokedex_data = json.load(f)

added = 0
for name in class_names:
    if name not in pokedex_data:
        pokedex_data[name] = {
            "type": "Unknown",
            "evolves_to": "None",
            "desc": "No description available.",
            "hp": 0,
            "attacks": []
        }
        added += 1

if added > 0:
    with open(POKEDEX_FILE, "w") as f:
        json.dump(pokedex_data, f, indent=2)
    print(f"✅ Added {added} missing Pokémon to pokedex_data.json!")
else:
    print("✅ All Pokémon in class_names.txt are present in pokedex_data.json.") 