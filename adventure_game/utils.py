from __future__ import annotations
from typing import (
    Any, Callable, Dict, Iterable, List, Optional, Tuple, TYPE_CHECKING
)

from . import compass
if TYPE_CHECKING:
    from .player import Player


class InvalidInstruction(Exception):
    pass


def print_options(options: Iterable[Any]):
    """
    Prints the options, numbered 1 to len(options).

    """
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")


def show_inventory(player: Player, *args):
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


def eat(player: Player, *args):
    try:
        option = int(args[0])
    except ValueError:
        print("eat must be followed by a number")
        return
    if option <= len(player.foods):
        food = player.foods[option - 1]
        print(f"You ate the {food.name}. {food.consume_msg}.")
        if food.restore_amount > 0:
            print(f"You gained {food.restore_amount} hp!")
        else:
            print(f"You lost {abs(food.restore_amount)} hp!")
        player.eat(option - 1)
    else:
        print("You don't have that much food!")


def throw(player: Player, *args):
    if player.cur_weapon is not None:
        print(f"You just threw away your {player.cur_weapon}")
        player.throw()
    else:
        print("You are not holding any weapon right now")


def parse_item_spec(spec: str) -> Tuple:
    spec_dict = {"w": "weapon", "o": "outfit"}
    try:
        key = spec_dict[spec[0]]
    except KeyError:
        print("equip must be followed by w/o")
        return ()
    try:
        value = int(spec[1])
    except ValueError:
        print(f"{key} must be followed by a number, e.g. w1")
        return ()
    return key, value


def equip(player: Player, *args):
    ikey, ival = parse_item_spec(args[0])
    if ival <= len(player.inventory[ikey]):
        print(f"You equipped the {player.inventory[ikey][ival - 1].name}")
        player.equip(ikey, ival)
    else:
        print(f"You don't have {ikey} #{ival} yet")


def drop(player: Player, *args):
    ikey, ival = parse_item_spec(args[0])
    if ival <= len(player.inventory[ikey]):
        print(f"You dropped the {player.inventory[ikey][ival - 1].name}")
        player.drop(ikey, ival)
    else:
        print(f"You don't have {ikey} #{ival} yet")


GLOBAL_OPTIONS: Dict[str, Callable[[Player, ...], Any]] = {
    'items': show_inventory,
    'equip': equip,
    'drop': drop,
    'throw': throw,
    'me': print,
    'eat': eat,
}


def prompt_player(prompt: str, player: Player) -> Optional[str]:
    if not prompt.endswith(" "):
        prompt += " "
    instr = input(prompt)
    strings = instr.split(' ')
    option, args = strings[0], strings[1:]

    if option in GLOBAL_OPTIONS:
        GLOBAL_OPTIONS[option](player, *args)
        return None

    return instr


def get_user_int(prompt: str, player: Player) -> Optional[int]:
    inputs = prompt_player(prompt, player)
    if inputs is None:
        return None

    return int(inputs)


def get_user_instr(
        prompt: str, player: Player
) -> Optional[Tuple[str, List[str]]]:
    """
    Prompts the user for input, and handles generic actions.

    Args:
        prompt: The message with which to prompt the user for input.
        player: The Player instance associated with the current user.

    Returns:
        None, if the input is a handled global option, otherwise a tuple
        containing the instruction command and a list of extra options.

    """
    inputs = prompt_player(prompt, player)
    if inputs is None:
        return None

    strings = inputs.split(' ')
    return strings[0], strings[1:]


def parse_movement_instr(
        instr: str, dest: str
) -> Optional[compass.Direction]:
    """
    Parses an instruction of the form 'go Direction' to extract the
    destination.

    Args:
        instr: The user's string input.
        dest: The direction in which to move.

    Returns:
        The direction in which to travel.

    """
    if instr == 'go':
        try:
            return compass.Direction[dest.capitalize()]
        except KeyError:
            # Continue to report invalid instruction
            raise InvalidInstruction(f"{dest} is not a valid direction")
    raise InvalidInstruction("Expected an instruction in the form: go north")
