from . import utils
from .compass import Direction
from .player import Player
from .room import generate_first_room


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
            action_id = None
            while action_id is None:
                utils.print_options(options.keys())
                action_id = utils.get_user_input(
                    "Which action would you like to do?",
                    player
                )
            key = list(options.keys())[int(action_id) - 1]
            # Invoke the action handler for the selected option
            options[key](player)

        exits = player.current_room.get_exits()
        exit_idx = None
        while exit_idx is None:
            print("Where would you like to go?")
            utils.print_options(exits)
            exit_idx = utils.get_user_input("Enter your choice:", player)
        dest = Direction[exits[exit_idx - 1]]
        player.go(dest)
