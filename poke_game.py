import json
import requests

import requests

url = 'https://pokeapi.co/api/v2/pokemon/?limit=150&offset=0'
response = requests.get(url)
pokemon_list = response.json()['results']

pokemon_name = input('Give me a Pokémon: ')

for pokemon in pokemon_list:
    if pokemon['name'] == pokemon_name.lower():
        pokemon_url = pokemon['url']
        pokemon_data = requests.get(pokemon_url).json()
        print("Name:", pokemon_name.capitalize())
        print("Stats:")
        for stat in pokemon_data['stats']:
            print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
        break
else:
    print("Pokémon not found:", pokemon_name.capitalize())


