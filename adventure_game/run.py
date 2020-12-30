from typing import Iterable

from .compass import Direction
from .player import Player
from .room import generate_first_room


def print_options(options: Iterable[str]):
    """
    Prints the options, numbered 1 to len(options).

    """
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")


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
            # TODO: some of the actions require further thought, e.g.:
            #    - fight loop for attacking enemies
            #    - printing treasure chest contents and allowing the player to
            #      pick up the items (removing them from the chest)
            options[key](player)

        print("Where would you like to go?")
        exits = player.current_room.get_exits()
        print_options(exits)
        dest = Direction[exits[int(input("Enter you choice: ")) - 1]]
        player.go(dest)
