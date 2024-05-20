import json
import requests
import random
import time
from prettytable import PrettyTable


url = 'https://pokeapi.co/api/v2/pokemon/?limit=150&offset=0' # URL to fetch Pokemon data
response = requests.get(url)
pokemon_list = response.json()['results'] # store data in variable


def get_pokemon_info(pokemon_name): # function to get full stats for a Pokémon
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}' # handle case sensitivity
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        print("Full Stats")
        print(f"Name: {pokemon_data['name'].capitalize()}")
        print(f"ID: {pokemon_data['id']}")
        print(f"Height: {pokemon_data['height']}")
        print(f"Weight: {pokemon_data['weight']}")

        print("Abilities:")
        for ability in pokemon_data['abilities']:
            print(f" - {ability['ability']['name'].capitalize()}")

        print("Moves:")
        move_list = [move['move']['name'].capitalize() for move in pokemon_data['moves']] # create move list
        print("\n".join([" - " + move for move in move_list]))

        print("Types:")
        type_list = [type_info['type']['name'].capitalize() for type_info in pokemon_data['types']]
        print(", ".join(type_list))

    else:
        print("Pokemon not found.")


def is_valid_pokemon(pokemon_name): # function to check if the entered Pokémon name is valid
    return any(pokemon_name.lower() == pokemon['name'] for pokemon in pokemon_list)


def display_stats(player_number, pokemon_name, pokemon_data): # function to display stats of a Pokémon
    print(f"Player {player_number}'s Pokémon - {pokemon_name.capitalize()}")
    print("Stats:")
    table = PrettyTable(["Stat", "Value"]) # for better formatted table
    for stat in pokemon_data['stats']:
        table.add_row([stat['stat']['name'].capitalize(), stat['base_stat']])
    print(table)


while True: # main game loop
    while True:
        player1_name = input('Player 1, give me a Pokémon: ').capitalize()
        if is_valid_pokemon(player1_name):
            break
        else:
            print("Invalid Pokémon name. Please try again.")

    player2_name = random.choice(pokemon_list)['name'] # random selection for CPU character

    player1_stats = {} # empty dictionary to store player 1 stats
    player2_stats = {}


    for pokemon in pokemon_list:     # fetch and display stats for Player 1's Pokémon
        if pokemon['name'] == player1_name.lower():
            player1_url = pokemon['url']
            player1_data = requests.get(player1_url).json()
            player1_stats = {stat['stat']['name']: stat['base_stat'] for stat in player1_data['stats']} # add to dict
            display_stats(1, player1_name, player1_data)
            break
    else:
        print("Player 1's Pokémon not found:", player1_name.capitalize())


    for pokemon in pokemon_list:
        if pokemon['name'] == player2_name.lower():
            player2_url = pokemon['url']
            player2_data = requests.get(player2_url).json()
            player2_stats = {stat['stat']['name']: stat['base_stat'] for stat in player2_data['stats']}
            display_stats(2, player2_name, player2_data)
            break
    else:
        print("Player 2's Pokémon not found:", player2_name.capitalize())

    player1_hp = player1_stats.get('hp', 0)
    player2_hp = player2_stats.get('hp', 0)

    choice = input("Do you want to view the full stats of your Pokémon? (yes/no): ").lower()
    if choice == "yes":
        get_pokemon_info(player1_name)
        get_pokemon_info(player2_name)
        input("Press Enter to continue...")

    while player1_hp > 0 and player2_hp > 0: # player 1 attack
        damage_to_player2 = max(1, player1_stats.get('attack', 0) - player2_stats.get('defense', 0))
        player2_hp -= damage_to_player2
        print(
            f"{player1_name.capitalize()} attacks {player2_name.capitalize()}! Remaining HP for {player1_name.capitalize()}: {player1_hp}, Remaining HP for {player2_name.capitalize()}: {player2_hp}")

        if player2_hp <= 0:
            print(f"{player1_name.capitalize()} wins!")
            break

        time.sleep(1) # time delay between attack rounds

        damage_to_player1 = max(1, player2_stats.get('attack', 0) - player1_stats.get('defense', 0)) # player 2 attack
        player1_hp -= damage_to_player1
        print(
            f"{player2_name.capitalize()} attacks {player1_name.capitalize()}! Remaining HP for {player1_name.capitalize()}: {player1_hp}, Remaining HP for {player2_name.capitalize()}: {player2_hp}")

    if player1_hp <= 0 and player2_hp <= 0: # draw
        print("It's a tie!")
    elif player1_hp <= 0: # player 2 wins
        print(f"{player2_name.capitalize()} wins!")
    elif player2_hp <= 0: # player 1 wins
        print(f"{player1_name.capitalize()} wins!")

    play_again = input("Do you want to play again? (yes/no): ").lower() # option to play again
    if play_again != "yes":
        break

