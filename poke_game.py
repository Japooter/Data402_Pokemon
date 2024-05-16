import json
import requests
import random

url = 'https://pokeapi.co/api/v2/pokemon/?limit=150&offset=0'
response = requests.get(url)
pokemon_list = response.json()['results']


def get_pokemon_info(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()

        print(f"Name: {pokemon_data['name'].capitalize()}")
        print(f"ID: {pokemon_data['id']}")
        print(f"Height: {pokemon_data['height']}")
        print(f"Weight: {pokemon_data['weight']}")

        print("Abilities:")
        for ability in pokemon_data['abilities']:
            print(f" - {ability['ability']['name'].capitalize()}")

        print("Moves:")
        move_list = [move['move']['name'].capitalize() for move in pokemon_data['moves']]
        print("\n".join([" - " + move for move in move_list]))

        print("Types:")
        type_list = [type_info['type']['name'].capitalize() for type_info in pokemon_data['types']]
        print(", ".join(type_list))

        print("Stats:")
        for stat in pokemon_data['stats']:
            print(f" - {stat['stat']['name'].capitalize()}: {stat['base_stat']}")

    else:
        print("Pokemon not found.")

def is_valid_pokemon(pokemon_name):
    return any(pokemon_name.lower() == pokemon['name'] for pokemon in pokemon_list)

while True:
    while True:
        player1_name = input('Player 1, give me a Pokémon: ').capitalize()
        if is_valid_pokemon(player1_name):
            break
        else:
            print("Invalid Pokémon name. Please try again.")

    player2_name = random.choice(pokemon_list)['name']

    player1_stats = {}
    player2_stats = {}

    for pokemon in pokemon_list:
        if pokemon['name'] == player1_name.lower():
            player1_url = pokemon['url']
            player1_data = requests.get(player1_url).json()
            player1_stats = {stat['stat']['name']: stat['base_stat'] for stat in player1_data['stats']}

            player1_pokemon_name = player1_data['name']
            player1_pokemon_types = [t['type']['name'] for t in player1_data['types']]
            print("Player 1's Pokémon -", player1_name.capitalize())
            print("Stats:")
            for stat, value in player1_stats.items():
                print(f"{stat.capitalize()}: {value}")
            print(f"Name: {player1_pokemon_name.capitalize()}")
            print("Types:", ", ".join(player1_pokemon_types))
            break
    else:
        print("Player 1's Pokémon not found:", player1_name.capitalize())

    for pokemon in pokemon_list:
        if pokemon['name'] == player2_name.lower():
            player2_url = pokemon['url']
            player2_data = requests.get(player2_url).json()
            player2_stats = {stat['stat']['name']: stat['base_stat'] for stat in player2_data['stats']}

            player2_pokemon_name = player2_data['name']
            player2_pokemon_types = [t['type']['name'] for t in player2_data['types']]
            print("\nPlayer 2's Pokémon -", player2_name.capitalize())
            print("Stats:")
            for stat, value in player2_stats.items():
                print(f"{stat.capitalize()}: {value}")
            print(f"Name: {player2_pokemon_name.capitalize()}")
            print("Types:", ", ".join(player2_pokemon_types))
            break
    else:
        print("Player 2's Pokémon not found:", player2_name.capitalize())

    player1_hp = player1_stats.get('hp', 0)
    player2_hp = player2_stats.get('hp', 0)

    choice = input("Do you want to view stats of your Pokémon? (yes/no): ").lower()
    if choice == "yes":
        get_pokemon_info(player1_name)
        get_pokemon_info(player2_name)
        input("Press Enter to continue...")

    while player1_hp > 0 and player2_hp > 0:
        damage_to_player2 = max(1, player1_stats.get('attack', 0) - player2_stats.get('defense', 0))
        player2_hp -= damage_to_player2
        print(f"{player1_name.capitalize()} attacks {player2_name.capitalize()}! Remaining HP for {player1_name.capitalize()}: {player1_hp}, Remaining HP for {player2_name.capitalize()}: {player2_hp}")

        if player2_hp <= 0:
            print(f"{player1_name.capitalize()} wins!")
            break

        damage_to_player1 = max(1, player2_stats.get('attack', 0) - player1_stats.get('defense', 0))
        player1_hp -= damage_to_player1
        print(f"{player2_name.capitalize()} attacks {player1_name.capitalize()}! Remaining HP for {player1_name.capitalize()}: {player1_hp}, Remaining HP for {player2_name.capitalize()}: {player2_hp}")

    if player1_hp <= 0 and player2_hp <= 0:
        print("It's a tie!")
    elif player1_hp <= 0:
        print(f"{player2_name.capitalize()} wins!")
    elif player2_hp <= 0:
        print(f"{player1_name.capitalize()} wins!")

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != "yes":
        break

