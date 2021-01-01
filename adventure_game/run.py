from . import messages, utils
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
        dest = None
        while dest is None:
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
        player.go(dest)
