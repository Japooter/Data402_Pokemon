import json
from random import randint
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

random_number = randint(1, 151)
url_computer = f'https://pokeapi.co/api/v2/pokemon/{random_number}'
pokemon_computer_data = requests.get(url_computer).json()
print("Name:", pokemon_computer_data['name'].capitalize())
print("Stats:")
for stat in pokemon_computer_data['stats']:
    print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")




