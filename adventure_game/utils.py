from __future__ import annotations
from typing import Iterable, Optional, TYPE_CHECKING

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
    if not len(player.inventory):
        print("You have NOTHING for the moment")

    else:
        print("Your inventory: ")
        print_options([t.name for t in player.inventory])
        print()


def equip(player: Player):
    option = get_user_input("Which item do you want to equip?", player)
    if option is not None:
        item = player.inventory[option - 1]
        player.equip(option)
        print(f"You equipped the {item.name}")


def get_user_input(prompt: str, player: Player) -> Optional[int]:
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

    while True:
        try:
            return int(option)
        except ValueError:
            print("You must enter an integer!")
            option = input(prompt)
