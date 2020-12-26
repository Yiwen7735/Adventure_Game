from .player import Player
from . import room

def run_game():
    name = input("Please enter your name: ")
    player = Player(name, 100)

    curr_room = room.generate_room()
    print(curr_room)

    options = curr_room.get_options()
    for i, option in enumerate(options.keys()):
        print(f"{i + 1}. {option}")

    action_id = input("Which action would you like to do?")
    key = list(options.keys())[action_id - 1]
    options[key](player)