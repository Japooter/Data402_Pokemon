import json
import random
import requests
import time

url = 'https://pokeapi.co/api/v2/pokemon/?limit=150&offset=0'
response = requests.get(url)
pokemon_list = response.json()['results']

player1_name = input('Player 1, give me a Pokémon: ')
player2_name = random.choice(pokemon_list)['name']

print("Player 2 (CPU) has selected:", player2_name.capitalize())

player1_stats = {} #empty dictionaries for pokemon stats
player2_stats = {}

for pokemon in pokemon_list:
    if pokemon['name'] == player1_name.lower():
        player1_url = pokemon['url']
        player1_data = requests.get(player1_url).json()
        player1_stats = {stat['stat']['name']: stat['base_stat'] for stat in player1_data['stats']}
        print("Player 1's Pokémon -", player1_name.capitalize())
        print("Stats:")
        for stat, value in player1_stats.items():
            print(f"{stat.capitalize()}: {value}")
        break
else:
    print("Player 1's Pokémon not found:", player1_name.capitalize())

for pokemon in pokemon_list:
    if pokemon['name'] == player2_name.lower():
        player2_url = pokemon['url']
        player2_data = requests.get(player2_url).json()
        player2_stats = {stat['stat']['name']: stat['base_stat'] for stat in player2_data['stats']}
        print("\nPlayer 2's Pokémon -", player2_name.capitalize())
        print("Stats:")
        for stat, value in player2_stats.items():
            print(f"{stat.capitalize()}: {value}")
        break
else:
    print("Player 2's Pokémon not found:", player2_name.capitalize())


player1_hp = player1_stats['hp'] # health points
player2_hp = player2_stats['hp']

pl1_chances = 0
pl2_chances = 0

while player1_hp > 0 and player2_hp > 0: #battle is a loop until there's a winner

    # p1 attacks p2, then p2 attacks p1
    pl1_attack= input('Choose:\n- Attack\n- Special-attack').lower()
    if pl1_attack == 'special-attack':
        pl1_chances +=1
    if pl1_chances > 2:
        if pl1_attack == 'special-attack':
            print(f'Sorry, no more special attacks available.')
        pl1_attack = 'attack'


    player2_hp -= max(1, player1_stats[pl1_attack] - player2_stats['defense'])
    print(f"{player1_name.capitalize()} attacks {player2_name.capitalize()} with {pl1_attack}!")
    time.sleep(2)
    # damage = attacker's Attack - defender's Defense stat
    # if positive, attacker deals at least 1 damage
    # if negative, the attacker deals 1 damage
    if player2_hp <= 0:
        print(f"{player1_name.capitalize()} wins!")
        break

    pl2_attack = random.choice(['attack', 'special-attack'])
    if pl2_attack == 'special-attack':
        pl2_chances +=1
    if pl2_chances > 2:
        pl2_attack = 'attack'
    player1_hp -= max(1, player2_stats[pl2_attack] - player1_stats['defense'])
    print(f"{player2_name.capitalize()} attacks {player1_name.capitalize()} with {pl2_attack}!")
    time.sleep(2)

if player1_hp <= 0 and player2_hp <= 0: # if both players health is zero
    print("It's a tie!")
elif player1_hp <= 0: # if p1 has less health
    print(f"{player2_name.capitalize()} wins!")
elif player2_hp <= 0: # if p2 has less health
    print(f"{player1_name.capitalize()} wins!")
