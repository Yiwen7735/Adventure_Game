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
    Enter a loop of attack between player and enemy, consisting of
        - 1. if the player is killed, game over
        - 2. remind the player if their hp falls below 10
        - 3. remind the player if their weapon is broken
        - 4. if enemy isn't killed, attacks back
        - 5. display hp status at the end of each mutual attack

    Args:
        player: the player in the game
        enemy: the enemy encountered in a certain room

    """
    option = "a"
    while option != "f":
        if not player.is_alive():
            break
        if player.hp < 10:
            run = None
            while run is None:
                run = get_user_input(
                    "RUN AWAY?? 1.Hell yeah  "
                    "2.Nope, gonna fight till I die",
                    player
                )
            if run == 1:
                player.retreat()
                break

        if option == "a":
            try:
                player.attack(enemy)
            except WeaponBrokenException:
                print(f"Your weapon is broken. Better run before {enemy.name} gets you")
            else:
                weapon_name = (
                    player.equipped["weapon"].name
                    if player.equipped["weapon"] is not None
                    else 'fists'
                )
                print(f"You attacked {enemy.name} with your {weapon_name}")

            if not enemy.is_alive():
                print(f"You took down the {enemy.name}!")
                break

            enemy.attack(player)

            print(
                f"hp stats: {player.name} {player.hp}, {enemy.name} {enemy.hp}"
            )

        option = get_user_input("Press 'a' to continue attacking or 'f' to flee", player)

    if option == 'f':
        print(f"You fled from the {enemy.name}. Better luck next time!")
        player.retreat()


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
        option = get_user_input("Press 'a' to take all or 'n' to take none", player)
        if option is None:
            continue

        if option == 'a':
            for treasure in chest.contents:
                print(f"You picked up {treasure.name}!")
                player.pick_up_item(treasure)
            chest.contents.clear()
        elif option == 'n':
            break
        else:
            treasure = chest.contents[option - 1]
            print(f"You picked up {treasure.name}!")
            player.pick_up_item(treasure)
            chest.contents.remove(treasure)

        if len(chest.contents) > 0:
            take_again = None
            while take_again is None:
                take_again = get_user_input("Continue to take?\n1. Yes \n2. No", player)
            if take_again == 2:
                break
