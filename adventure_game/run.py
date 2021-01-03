from . import messages, utils
from .player import Player
from .room import generate_first_room, NoSuchExitException
import sys


def game_over():
    print("You were relentlessly killed. RIP.")
    sys.exit(0)


def run_game():
    name = input("Please enter your name: ")
    player = Player(name, 100)

    # Move the player to the starting room
    player.move_to(generate_first_room())

    while player.is_alive():
        messages.print_enter(player.current_room)
        options = player.current_room.get_options()
        if options:
            action_id = None
            while action_id is None:
                messages.print_options(options)
                action_id = utils.get_user_input(
                    "What would you like to do?",
                    player
                )
            # Invoke the action handler for the selected option
            options[action_id].handler(player)

        exits = player.current_room.exits
        dest = None
        while dest is None and player.is_alive():
            print(
                "There are portals to the "
                f"{messages.list_to_comma_string(exits)}."
            )
            instr = utils.get_user_input(
                "What would you like to do?",
                player
            )
            if instr is None:
                continue
            dest = utils.parse_movement_instr(instr)
            if dest is not None:
                try:
                    player.go(dest)
                except NoSuchExitException:
                    print(f"There is no portal to the {dest}.")
                    dest = None

    game_over()
