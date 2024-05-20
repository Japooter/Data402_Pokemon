import json
import requests
import random
import time

url = 'https://pokeapi.co/api/v2/pokemon/?limit=150&offset=0'
response = requests.get(url)
pokemon_list = response.json()['results']

def get_pokemon_info(pokemon_name): # get full stats for pokemon in fight
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
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
while True:
    player1_chosen = False
    while player1_chosen == False:
        choice_of_players = input("How many players? (1/2) \n")
        if choice_of_players == "1":

            player1_name = input('Player 1, give me a Pokémon: ')
            player2_name = random.choice(pokemon_list)['name']
            player1_chosen = True

            #print("Player 2 (CPU) has selected:", player2_name.capitalize())

        elif choice_of_players == "2":

            player1_name = input('Player 1, give me a Pokémon: ')
            # player2_name = input('Player 2, give me a Pokémon: ')
            player1_chosen = True
        else:
            print("Invalid input.\n")

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
                final_check = input("Are you happy with this choice? [y/n]\n")
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
                    final_check = input("Are you happy with this choice? [y/n]\n")
                    if final_check == 'n' or final_check == 'no' or final_check == '2':
                        p2_check = False
                        player2_name = input("Give me a Pokémon: ")
                    break
        else:
            print("Player 2's Pokémon not found:", player2_name.capitalize())
            player2_name = input("Give me a Pokémon: ")


    player1_hp = player1_stats['hp'] # health points
    player2_hp = player2_stats['hp']

    player1_specialuses = 2
    player2_specialuses = 2

    full_stat_p1 = input("Player 1, do you want to view the full stats of your Pokémon? (yes/no): ").lower()
    if full_stat_p1 == "yes":
        get_pokemon_info(player1_name)
        input("Press Enter to continue...")

    if choice_of_players == "2":
        full_stat_p2 = input("Player 2, do you want to view the full stats of your Pokémon? (yes/no): ").lower()
        if full_stat_p2 == "yes":
            get_pokemon_info(player2_name)
            input("Press Enter to continue...")

    while player1_hp > 0 and player2_hp > 0: #battle is a loop until there's a winner
        # print(player1_stats)
        # print(player2_stats)
        p1_choice = input("Choose an action! \n"
                          "Attack \n"
                          "Special Attack \n")
        # p1 attacks p2, then p2 attacks p1
        #p1_choice = p1_choice.capitalize()
        if p1_choice == "Attack":
            player2_hp -= max(1, player1_stats['attack'] - player2_stats['defense'])
            print(f"{player1_name.capitalize()} attacks {player2_name.capitalize()}!")
            print(f"{player2_name.capitalize()}\'s HP: {player2_hp}")
        elif p1_choice == ("Special Attack"):
            if player1_specialuses > 0:
                player2_hp -= max(1, player1_stats['special-attack'] - player2_stats['special-defense'])
                print(f"{player1_name.capitalize()} uses their special attack on {player2_name.capitalize()}!")
                print(f"{player2_name.capitalize()}\'s HP: {player2_hp}")
                player1_specialuses -= 1
            else:
                print("Out of special attack uses! Resorting to regular attack!")
                player2_hp -= max(1, player1_stats['attack'] - player2_stats['defense'])
                print(f"{player1_name.capitalize()} attacks {player2_name.capitalize()}!")
                print(f"{player2_name.capitalize()}\'s HP: {player2_hp}")
        else:
            print("Invalid input, defaulting to Attack.")
            player2_hp -= max(1, player1_stats['attack'] - player2_stats['defense'])
            print(f"{player1_name.capitalize()} attacks {player2_name.capitalize()}!")
            print(f"{player2_name.capitalize()}\'s HP: {player2_hp}")
        time.sleep(1)
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
            #p2_choice = p2_choice.capitalize()
        elif choice_of_players == "1":
            p2_choice = random.choice(["Attack", "Special Attack"])
        if p2_choice == "Attack":
            player1_hp -= max(1, player2_stats['attack'] - player1_stats['defense'])
            print(f"{player2_name.capitalize()} attacks {player1_name.capitalize()}!")
            print(f"{player1_name.capitalize()}\'s HP: {player1_hp}")
        elif p2_choice == ("Special Attack"):
            if player2_specialuses > 0:
                player1_hp -= max(1, player2_stats['special-attack'] - player1_stats['special-defense'])
                print(f"{player2_name.capitalize()} uses their special attack on {player1_name.capitalize()}!")
                print(f"{player1_name.capitalize()}\'s HP: {player1_hp}")
                player2_specialuses -= 1
            else:
                print("Out of special attack uses! Resorting to regular attack!")
                player1_hp -= max(1, player2_stats['attack'] - player1_stats['defense'])
                print(f"{player2_name.capitalize()} attacks {player1_name.capitalize()}!")
                print(f"{player1_name.capitalize()}\'s HP: {player1_hp}")
        else:
            print("Invalid input, defaulting to Attack.")
            player1_hp -= max(1, player2_stats['attack'] - player1_stats['defense'])
            print(f"{player2_name.capitalize()} attacks {player1_name.capitalize()}!")
            print(f"{player1_name.capitalize()}\'s HP: {player1_hp}")
        time.sleep(1)

    if player1_hp <= 0 and player2_hp <= 0: # if both players health is zero
        print("It's a tie!")
    elif player1_hp <= 0: # if p1 has less health
        print(f"{player2_name.capitalize()} wins!")
    elif player2_hp <= 0: # if p2 has less health
        print(f"{player1_name.capitalize()} wins!")
    play_again = input("Would you like to play again? [y/n]\n")
    if play_again == "n":
        break
