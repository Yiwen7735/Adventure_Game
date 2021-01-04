import sys

from . import action, messages, utils
from .exceptions import NoSuchExitException
from .player import Player


def game_over():
    print("You were relentlessly killed. RIP.")
    sys.exit(0)


def run_game():
    name = input("Please enter your name: ")
    player = Player(name, 100)

    # Move the player to the starting room
    player.move_to_new_room()

    while player.is_alive():
        messages.print_enter(player.current_room)
        if player.current_room.trap is not None:
            # If the trap is triggered, start the loop again (check alive. printing, etc)
            if action.trigger_trap(player, player.current_room.trap):
                continue

        options = player.current_room.get_options()
        if options:
            while True:
                messages.print_options(options)
                inputs = utils.get_user_instr(
                    "What would you like to do?",
                    player
                )
                if inputs is None:
                    # Global option handled in get_user_instr
                    continue
                action_id = inputs[0]
                # Invoke the action handler for the selected option
                try:
                    options[action_id].handler(player)
                except KeyError:
                    print(f"Invalid instruction: {action_id}")
                else:
                    break

        exits = player.current_room.exits
        while player.is_alive():
            print(
                "There are portals to the "
                f"{messages.list_to_comma_string(exits)}."
            )
            instr = utils.get_user_instr(
                "What would you like to do?",
                player
            )
            if instr is None:
                continue
            instr, args = instr
            if not args:
                print("Expected an instruction in the form: go north")
                continue

            try:
                dest = utils.parse_movement_instr(instr, args[0])
            except utils.InvalidInstruction as e:
                print(e)
                continue

            try:
                player.go(dest)
            except NoSuchExitException:
                print(f"There is no portal to the {dest}.")
            else:
                break

    game_over()
