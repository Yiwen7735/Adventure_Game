from __future__ import annotations
from typing import Iterable, Optional, Union, TYPE_CHECKING

from . import compass
if TYPE_CHECKING:
    from .player import Player


def print_options(options: Iterable[str]):
    """
    Prints the options, numbered 1 to len(options).

    """
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")


def show_inventory(player: Player):
    """
    Display all the items the player has

    Args:
        player: the player in the game

    Returns:

    """
    for item_key, item_list in player.inventory.items():
        print(f"Your {item_key}s: ")
        if not len(item_list):
            print(f"You have NO {item_key}s")
        else:
            print_options(item_list)


def equip(player: Player):
    option = get_user_input("Which item do you want to equip? "
                            "[e.g., w1: weapon #1, o2: outfit #2]",
                            player)
    if option is not None:
        # TODO: should expand it for all options?
        option_dict = {"w": "weapon", "o": "outfit"}
        item_type = option_dict[option[0]]
        item_num = int(option[1])
        item_list = player.inventory[item_type]
        if item_num <= len(item_list):
            player.equip(item_type, item_num)
            print(f"You equipped the {item_list[item_num - 1].name}")
        else:
            print(f"No {item_type} found.")


def get_user_input(prompt: str, player: Player) -> Optional[Union[int, str]]:
    """
    Prompts the user for input, and handles generic actions.

    The following inputs are handled specially:
      - i: Print the player's inventory
      - e: Equip an item (weapon/outfit)
    If the input is not one of these characters, it is cast to an integer
    and returned for the caller to handle.

    Args:
        prompt: The message with which to prompt the user for input.
        player: The Player instance associated with the current user.

    Returns:
        None, if the input is handled here, int otherwise.

    """
    if not prompt.endswith(" "):
        prompt += " "
    option = input(prompt)
    if option == 'i':
        show_inventory(player)
        return None

    if option == 'e':
        equip(player)
        return None

    try:
        return int(option)
    except ValueError:
        return option


def parse_movement_instr(instr: str) -> Optional[compass.Direction]:
    """
    Parses an instruction of the form 'go Direction' to extract the
    destination.

    Args:
        instr: The user's string input.

    Returns:
        The direction in which to travel.

    """
    if instr.startswith('go '):
        try:
            return compass.Direction[instr[3:].capitalize()]
        except KeyError:
            # Continue to report invalid instruction
            pass
    print("Expected an instruction in the form: go north")
    return None
