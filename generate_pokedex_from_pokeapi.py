import requests
import json

POKEDEX_FILE = "backend/pokedex_data.json"
GEN1_COUNT = 151

pokedex = {}

for i in range(1, GEN1_COUNT + 1):
    # Fetch main Pokémon data
    poke_url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{i}/"
    poke_resp = requests.get(poke_url).json()
    species_resp = requests.get(species_url).json()

    name = poke_resp['name'].capitalize()
    types = [t['type']['name'].capitalize() for t in poke_resp['types']]
    type_str = "/".join(types)
    hp = next(stat['base_stat'] for stat in poke_resp['stats'] if stat['stat']['name'] == 'hp')
    # Get up to 4 unique level-up moves
    moves = [m['move']['name'].replace('-', ' ').title() for m in poke_resp['moves']]
    moves = list(dict.fromkeys(moves))[:4]
    # Get English Pokédex description
    desc = next((e['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                 for e in species_resp['flavor_text_entries'] if e['language']['name'] == 'en'), "No description available.")
    # Get next evolution (if any)
    evo_chain_url = species_resp['evolution_chain']['url']
    evo_chain = requests.get(evo_chain_url).json()['chain']
    def find_next_evo(chain, current):
        if chain['species']['name'] == current:
            if chain['evolves_to']:
                return chain['evolves_to'][0]['species']['name'].capitalize()
            else:
                return "None"
        for evo in chain['evolves_to']:
            result = find_next_evo(evo, current)
            if result:
                return result
        return None
    next_evo = find_next_evo(evo_chain, poke_resp['name']) or "None"

    pokedex[name] = {
        "type": type_str,
        "evolves_to": next_evo,
        "desc": desc,
        "hp": hp,
        "attacks": moves
    }
    print(f"Fetched {name}")

with open(POKEDEX_FILE, "w") as f:
    json.dump(pokedex, f, indent=2)

print(f"✅ Generated {POKEDEX_FILE} with {len(pokedex)} Pokémon!") 