import json

# List of all 151 Gen 1 Pokémon in order
GEN1_POKEMON = [
    'Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard',
    'Squirtle', 'Wartortle', 'Blastoise', 'Caterpie', 'Metapod', 'Butterfree',
    'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto', 'Pidgeot',
    'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 'Pikachu',
    'Raichu', 'Sandshrew', 'Sandslash', 'Nidoran♀', 'Nidorina', 'Nidoqueen',
    'Nidoran♂', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable', 'Vulpix',
    'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish',
    'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Venonat', 'Venomoth',
    'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck',
    'Mankey', 'Primeape', 'Growlithe', 'Arcanine', 'Poliwag', 'Poliwhirl',
    'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 'Machoke',
    'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool',
    'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash',
    'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', 'Farfetchd', 'Doduo',
    'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster',
    'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby',
    'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone',
    'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Weezing',
    'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea',
    'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie', 'Mr. Mime',
    'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros',
    'Magikarp', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon',
    'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto',
    'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres',
    'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew'
]

CLASS_FILE = "class_names.txt"
POKEDEX_FILE = "backend/pokedex_data.json"

with open(CLASS_FILE, "r") as f:
    class_names = [line.strip() for line in f if line.strip()]

with open(POKEDEX_FILE, "r") as f:
    pokedex_data = json.load(f)

missing = [name for name in GEN1_POKEMON if name not in class_names]
added = 0
for name in missing:
    if name not in pokedex_data:
        pokedex_data[name] = {
            "type": "Unknown",
            "evolves_to": "None",
            "desc": "No description available.",
            "hp": 0,
            "attacks": []
        }
        added += 1

if missing:
    print(f"Missing from class_names.txt ({len(missing)}): {', '.join(missing)}")
else:
    print("All 151 Gen 1 Pokémon are present in class_names.txt!")

if added > 0:
    with open(POKEDEX_FILE, "w") as f:
        json.dump(pokedex_data, f, indent=2)
    print(f"✅ Added {added} missing Gen 1 Pokémon to pokedex_data.json!")
else:
    print("No new entries needed in pokedex_data.json.") 