from .compass import Direction
from .player import Player
from .room import generate_first_room
from .utils import print_options


def game_over():
    pass


def run_game():
    name = input("Please enter your name: ")
    player = Player(name, 100)

    # Move the player to the starting room
    player.move_to(generate_first_room())

    while True:
        print("You enter " + str(player.current_room) + ".")
        options = player.current_room.get_options()
        if options:
            print_options(options.keys())
            action_id = input("Which action would you like to do?")
            key = list(options.keys())[int(action_id) - 1]
            # Invoke the action handler for the selected option
            options[key](player)

        print("Where would you like to go?")
        exits = player.current_room.get_exits()
        print_options(exits)
        dest = Direction[exits[int(input("Enter you choice: ")) - 1]]
        player.go(dest)
