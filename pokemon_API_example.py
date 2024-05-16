# import json
# import random
# import requests
# import os
#
#
# url = 'https://pokeapi.co/api/v2/pokemon/?limit=150&offset=0'
# response = requests.get(url)
# pokemon_list = response.json()['results']
#
# print(pokemon_list)
#
# #cpu_pok_id = random.randint(1, 150)
#
# #pok_cpu_url = f'https://pokeapi.co/api/v2/pokemon/{str(cpu_pok_id)}'
# cpu_pok = random.choice(pokemon_list)['name']
#
# for pokebot in pokemon_list:
#     if pokebot['name'] == cpu_pok.lower():
#         #print(pokebot['url'])
#         cpu_url = pokebot['url']
#         print(cpu_url)
#         cpu_name = pokebot['name']
#         cpu_data = requests.get(cpu_url).json()
#
#
#
# pokemon_name = input('Give me a Pokémon: ')
# input_check = False
# while input_check == False:
#     for pokemon in pokemon_list:
#         if pokemon['name'] == pokemon_name.lower():
#             input_check = True
#             pokemon_url = pokemon['url']
#             pokemon_data = requests.get(pokemon_url).json()
#             print("Name:", pokemon_name.capitalize())
#             print("Stats:")
#             for stat in pokemon_data['stats']:
#                 print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
#             final_check = input('Are you happy with this choice? [y/n]')
#             if final_check == 'n' or final_check == 'no' or final_check == '2':
#                 input_check = False
#                 pokemon_name = input('Give me a Pokémon: ')
#
#             break
#     else:
#         print("Pokémon not found:", pokemon_name.capitalize())
#         pokemon_name = input('Give me a Pokémon: ')
#
# if input_check:
#     print("Let the battle begin!\n")
#     print("Your stats: ")
#     print("Name:", pokemon_name.capitalize())
#     print("Stats:")
#     for stat in pokemon_data['stats']:
#         print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}\n")
#
#
#     print("Your opponent: ")
#     print("Name:", cpu_name.capitalize())
#     print("Stats:")
#     for stat in cpu_data['stats']:
#         print(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")


import json
import requests
import random

url = 'https://pokeapi.co/api/v2/pokemon/?limit=150&offset=0'
response = requests.get(url)
pokemon_list = response.json()['results']
choice_of_players = input("How many players? (1/2) \n")
if choice_of_players == "1":

    player1_name = input('Player 1, give me a Pokémon: ')
    player2_name = random.choice(pokemon_list)['name']

    #print("Player 2 (CPU) has selected:", player2_name.capitalize())

elif choice_of_players == "2":

    player1_name = input('Player 1, give me a Pokémon: ')
    # player2_name = input('Player 2, give me a Pokémon: ')

player1_stats = {} #empty dictionaries for pokemon stats
player2_stats = {}
p1_check = False
while p1_check == False:
    for pokemon in pokemon_list:
        if pokemon['name'] == player1_name.lower():
            p1_check = True
            player1_url = pokemon['url']
            player1_data = requests.get(player1_url).json()
            player1_stats = {stat['stat']['name']: stat['base_stat'] for stat in player1_data['stats']}
            print("Player 1's Pokémon -", player1_name.capitalize())
            print("Stats:")
            for stat, value in player1_stats.items():
                print(f"{stat.capitalize()}: {value}")
            final_check = input("Are you happy with this choice? [y/n]")
            if final_check == 'n' or final_check == 'no' or final_check == '2':
                p1_check = False
                player1_name = input("Give me a Pokémon: ")
            break
    #             final_check = input('Are you happy with this choice? [y/n]')
    #             if final_check == 'n' or final_check == 'no' or final_check == '2':
    #                 input_check = False
    #                 pokemon_name = input('Give me a Pokémon: ')
    #
    #             break
    else:
        print("Player 1's Pokémon not found:", player1_name.capitalize())
        player1_name = input("Give me a Pokémon: ")
if choice_of_players == "1":
    print("Player 2 (CPU) has selected:", player2_name.capitalize())

elif choice_of_players == "2":
    player2_name = input('Player 2, give me a Pokémon: ')
p2_check = False
while p2_check == False:
    for pokemon in pokemon_list:
        if pokemon['name'] == player2_name.lower():
            p2_check = True
            player2_url = pokemon['url']
            player2_data = requests.get(player2_url).json()
            player2_stats = {stat['stat']['name']: stat['base_stat'] for stat in player2_data['stats']}
            print("\nPlayer 2's Pokémon -", player2_name.capitalize())
            print("Stats:")
            for stat, value in player2_stats.items():
                print(f"{stat.capitalize()}: {value}")
            if choice_of_players == "2":
                final_check = input("Are you happy with this choice? [y/n]")
                if final_check == 'n' or final_check == 'no' or final_check == '2':
                    p2_check = False
                    player2_name = input("Give me a Pokémon: ")
                break
    else:
        print("Player 2's Pokémon not found:", player2_name.capitalize())
        player2_name = input("Give me a Pokémon: ")


player1_hp = player1_stats['hp'] # health points
player2_hp = player2_stats['hp']

while player1_hp > 0 and player2_hp > 0: #battle is a loop until there's a winner
    p1_choice = input("Choose an action! \n"
                      "Attack \n"
                      "Special Attack \n")
    # p1 attacks p2, then p2 attacks p1
    p1_choice = p1_choice.capitalize()
    if p1_choice == "Attack":
        player2_hp -= max(1, player1_stats['attack'] - player2_stats['defense'])
        print(f"{player1_name.capitalize()} attacks {player2_name.capitalize()}!")
        print(f"{player2_name.capitalize()}\'s HP: {player2_hp}")
    elif p1_choice == "Special Attack":
        player2_hp -= max(1, player1_stats['special-attack'] - player2_stats['special-defense'])
        print(f"{player1_name.capitalize()} attacks {player2_name.capitalize()}!")
        print(f"{player2_name.capitalize()}\'s HP: {player2_hp}")
    # damage = attacker's Attack - defender's Defense stat
    # if positive, attacker deals at least 1 damage
    # if negative, the attacker deals 1 damage
    if player2_hp <= 0:
        print(f"{player1_name.capitalize()} wins!")
        break
    if choice_of_players == "2":
        p2_choice = input("Choose an action! \n"
                         "Attack \n"
                         "Special Attack \n")
        p2_choice = p2_choice.capitalize()
    elif choice_of_players == "1":
        p2_choice = random.choice(["Attack", "Special Attack"])
    if p2_choice == "Attack":
        player1_hp -= max(1, player2_stats['attack'] - player1_stats['defense'])
        print(f"{player2_name.capitalize()} attacks {player1_name.capitalize()}!")
        print(f"{player1_name.capitalize()}\'s HP: {player1_hp}")

if player1_hp <= 0 and player2_hp <= 0: # if both players health is zero
    print("It's a tie!")
elif player1_hp <= 0: # if p1 has less health
    print(f"{player2_name.capitalize()} wins!")
elif player2_hp <= 0: # if p2 has less health
    print(f"{player1_name.capitalize()} wins!")