import requests
import json

url = 'https://pokeapi.co/api/v2/pokemon/?limit=150&offset=0'
response = requests.get(url)
pokemon_list = json.loads(response.text)['results']

pokemon = input('give me a pokemon')

for n in pokemon_list:
    if n['name'] == pokemon:
        response = requests.get(n['url'])
        print(response.json())


