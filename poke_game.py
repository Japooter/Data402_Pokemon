import random
import requests
import json
from random import randint

# Get the list of pokemon from the API
url = 'https://pokeapi.co/api/v2/pokemon/?limit=150&offset=0'
response = requests.get(url)
pokemon_list = response.json()['results']

pokemon_list

def get_player_pokemon():
    pokemon_name = input('Please enter a pokemon: ')
    global player_pokemon_stats
    global pokemon_data
    player_pokemon_stats = {}
    for pokemon in pokemon_list:
        if pokemon['name'] == pokemon_name.lower():
            pokemon_url = pokemon['url']
            pokemon_data = requests.get(pokemon_url).json()
            player_pokemon_stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data["stats"]}
            print("You have chosen:", pokemon_name.capitalize())
            print("Stats:")
            for stat in pokemon_data['stats']:
                print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}\n")
            break
    else:
        print("Pokémon not found:", pokemon_name.capitalize())

def get_random_pokemon():

    global enemy_pokemon_stats
    global enemy_pokemon_data
    enemy_pokemon_stats = {}
    rng = randint(0, 150)
    enemy = f"https://pokeapi.co/api/v2/pokemon/{rng}/"
    enemy_pokemon_data = requests.get(enemy).json()
    enemy_pokemon_stats = {stat['stat']['name']: stat['base_stat'] for stat in enemy_pokemon_data["stats"]}
    print("Name:", enemy_pokemon_data["name"].capitalize())
    print("Stats:")
    for stat in enemy_pokemon_data['stats']:
        print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}\n")


def attack():
    player_pokemon = player_pokemon_stats
    enemy_pokemon = enemy_pokemon_stats
    while player_pokemon["hp"] > 0 and enemy_pokemon["hp"] > 0:
        if player_pokemon["speed"] > enemy_pokemon["speed"]:

            enemy_pokemon["hp"] -= max(1,player_pokemon["attack"] - enemy_pokemon["defense"])
            print(f"\n {pokemon_data["name"]} attacked {enemy_pokemon_data["name"]} for {max(1,player_pokemon["attack"] - enemy_pokemon["defense"])} "
                  f"\n  {enemy_pokemon_data["name"]} hp at {enemy_pokemon["hp"]}")

            if enemy_pokemon["hp"] > 0:
                player_pokemon["hp"] -= max(1,enemy_pokemon["attack"] - player_pokemon["defense"])
                print(f"\n {enemy_pokemon_data["name"]} attacked {pokemon_data["name"]} for {max(1,enemy_pokemon["attack"] - player_pokemon["defense"])} "
                      f"\n  {pokemon_data["name"]} hp at {player_pokemon["hp"]}")

        elif enemy_pokemon["speed"] > player_pokemon["speed"]:

            player_pokemon["hp"] -= max(1,enemy_pokemon["attack"] - player_pokemon["defense"])
            print(f"\n {enemy_pokemon_data["name"]} attacked {pokemon_data["name"]} for {max(1,player_pokemon["attack"] - enemy_pokemon["defense"])} "
                  f"\n  {pokemon_data["name"]} hp at {player_pokemon["hp"]} \n")

            if player_pokemon["hp"] > 0:
                enemy_pokemon["hp"] -= max(1,player_pokemon["attack"] - enemy_pokemon["defense"])
                print(f"\n{player_pokemon["name"]} attacked {enemy_pokemon["name"]} for {max(1,enemy_pokemon["attack"] - player_pokemon["defense"])} "
                      f"\n  {enemy_pokemon_data["name"]} hp at {enemy_pokemon["hp"]}")

    if enemy_pokemon["hp"] <= 0:
        print(f"{enemy_pokemon_data["name"]} fainted")
        print(f"{pokemon_data["name"]} wins")
        return

    if player_pokemon["hp"] <= 0:
        print(f"{pokemon_data["name"]} fainted")
        print(f"{enemy_pokemon_data["name"]} wins!")
        return



def pokemon_battle():
    get_player_pokemon()
    get_random_pokemon()
    attack()



pokemon_battle()