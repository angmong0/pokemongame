import random
import requests


def random_pokemon():
    pokemon_number = random.randint(1, 151)
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_number)
    response = requests.get(url)
    pokemon = response.json()

    return {
        'name': pokemon['name'],
        'id': pokemon['id'],
        'height': pokemon['height'],
        'weight': pokemon['weight'],
    }


def record_scores(round_number, user_pokemon, opponent_pokemon, user_stat, opponent_stat):
    with open('scores.txt', 'a') as file:
        file.write('Round {}: User: {} ({}), Opponent: {} ({}), Stat: {}\n'.format(
            round_number, user_pokemon['name'], user_pokemon['id'],
            opponent_pokemon['name'], opponent_pokemon['id'],
            user_stat, opponent_stat))


def select_pokemon():
    pokemon_options = []
    for _ in range(3):
        pokemon = random_pokemon()
        pokemon_options.append(pokemon)

    print("Choose your Pokemon:")
    for i, pokemon in enumerate(pokemon_options):
        print("{}. {}".format(i + 1, pokemon['name']))

    choice = input("Enter the number corresponding to your choice: ")
    choice_index = int(choice) - 1

    if choice_index >= 0 and choice_index < len(pokemon_options):
        return pokemon_options[choice_index]
    else:
        print("Invalid choice. Randomly selecting your Pokemon.")
        return random.choice(pokemon_options)


def run():
    global user_wins
    global opponent_wins

    user_wins = 0
    opponent_wins = 0

    my_pokemon = select_pokemon()
    print('For this battle, you chose {}'.format(my_pokemon['name']))

    opponent_pokemon = random_pokemon()
    print('The opponent chose {}'.format(opponent_pokemon['name']))

    while my_pokemon == opponent_pokemon:
        print("Opponent's Pokemon matches yours. Regenerating opponent's Pokemon...")
        opponent_pokemon = random_pokemon()
        print('The opponent chose {}'.format(opponent_pokemon['name']))

    for round_number in range(1, 4):
        valid_stat_choice = False
        while not valid_stat_choice:
            stat_choice = input('Which stat do you want to use to overpower your opponent? (id, height, weight): ')

            if stat_choice in ['id', 'height', 'weight']:
                valid_stat_choice = True
            else:
                print('Error: Incorrect stat. Please try again.')

        my_stat = my_pokemon[stat_choice]
        opponent_stat = opponent_pokemon[stat_choice]

        if my_stat > opponent_stat:
            print('Your opponent\'s stat was {} and yours was {}. You Win!'.format(opponent_stat, my_stat))
            user_wins += 1
        elif my_stat < opponent_stat:
            print('Your opponent\'s stat was {} and yours was {}. You Lose!'.format(opponent_stat, my_stat))
            opponent_wins += 1
        else:
            print('Your opponent\'s stat was {} and yours was {}. Draw!'.format(opponent_stat, my_stat))

        record_scores(round_number, my_pokemon, opponent_pokemon, my_stat, opponent_stat)


def final_score():
    if user_wins > opponent_wins:
        print('You won the match!')
    elif user_wins < opponent_wins:
        print('You lost the match!')
    else:
        print('The game ended in a tie!')

    my_pokemon = random_pokemon()
    opponent_pokemon = random_pokemon()
    record_scores(my_pokemon, opponent_pokemon, user_wins, opponent_wins)


run()
final_score()
