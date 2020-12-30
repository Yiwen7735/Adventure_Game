from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player
from .chest import Chest
from .enemy import Enemy
from .utils import print_options, get_user_input
from .weapon import WeaponBrokenException


def attack(player: Player, enemy: Enemy):
    """
    Enter a loop of attack between player and enemy

    Args:
        player: the player in the game
        enemy: the enemy encountered in a certain room

    """
    while player.is_alive() and enemy.is_alive():
        try:
            player.attack(enemy)
        except WeaponBrokenException:
            print("Your weapon is broken. Better run before he gets you")

        enemy.attack(player)

        print(f"hp stats: {player.name} {player.hp}, {enemy.name} {enemy.hp}")
        run = input("RUN AWAY?? 1.Hell yeah  2.Nope, gonna fight till I die")
        if run == '1':
            player.retreat()
            break


def collect(player: Player, chest: Chest):
    """
    Enter a loop of collecting items found in the chest

    Args:
        player: the player in the game
        chest: the chest found in a certain room

    """
    chest.open()

    if len(chest.contents) == 0:
        print("Bad luck! There is nothing in the chest")
        return

    print("Looks like you've found something...\n"
          "Which one would you like to take?")

    while len(chest.contents) > 0:
        print_options([t.name for t in chest.contents])
        if len(chest.contents) > 1:
            print(f"{len(chest.contents) + 1}. All of the above")

        option = get_user_input("", player)
        if option is None:
            continue

        if option > len(chest.contents):
            for treasure in chest.contents:
                player.pick_up_item(treasure)
            chest.contents.clear()

        else:
            treasure = chest.contents[option - 1]
            player.pick_up_item(treasure)
            chest.contents.remove(treasure)

        if len(chest.contents) > 0:
            take_again = None
            while take_again is None:
                take_again = get_user_input("Continue to take?\n1. Yes \n2. No", player)
            if take_again == 2:
                break
