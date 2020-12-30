from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

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
        player.equip(option)


def get_user_input(prompt: str, player: Player):
    option = input(prompt)
    if option == 'i':
        show_inventory(player)
        return None

    if option == 'e':
        equip(player)
        return None

    return int(option)

