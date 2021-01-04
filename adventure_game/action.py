from __future__ import annotations
import random
from typing import List, TYPE_CHECKING
import time

from . import constants, item, messages
from .chest import Chest
from .enemy import Enemy
from .exceptions import InventoryFullException, WeaponBrokenException
from .trap import Trap
from .utils import print_options, get_user_instr
if TYPE_CHECKING:
    from .player import Player


def attack(player: Player, enemy: Enemy):
    """
    Enter a loop of attack between player and enemy, consisting of
        - 1. if the player is killed, game over
        - 2. remind the player if their hp falls below 20
        - 3. remind the player if their weapon is broken
        - 4. if enemy isn't killed, attacks back
        - 5. display hp status at the end of each mutual attack

    Args:
        player: the player in the game
        enemy: the enemy encountered in a certain room

    """
    option = "a"
    while option != "f":
        if option == "a":
            try:
                player.attack(enemy)
            except WeaponBrokenException:
                print(
                    "Your weapon is BROKENNNN! Throw it away and RUNNN--"
                )
            else:
                weapon_name = (
                    player.equipped["weapon"].name
                    if player.equipped["weapon"] is not None
                    else 'fists'
                )
                print(
                    f"You attacked the {enemy.short_name} with your "
                    f"{weapon_name}"
                )

            if not enemy.is_alive():
                print(f"You took down the {enemy.short_name}!")
                break

            enemy.attack(player)
            print(
                f"The {enemy.short_name} attacked you with its "
                f"{enemy.weapon.name}"
            )

            print(
                f"hp stats: {player.name} {player.hp}, "
                f"{enemy.short_name} {enemy.hp}"
            )
            if not player.is_alive():
                break

        message = "Press 'a' to continue attacking or 'f' to flee."
        if player.hp < 20:
            message = "Your hp is at a dangerous level. RUN AWAY??"
        while (inputs := get_user_instr(message, player)) is None:
            continue
        option, _ = inputs

    if option == 'f':
        print(f"You fled from the {enemy.short_name}. Better luck next time!")
        retreat(player)


def take_loop(player: Player, items: List[item.Item]):
    """
    Enter a loop of collecting items from a list.

    Args:
        player: The Player in the game.
        items: The available items.

    """
    while len(items) > 0:
        print_options(items)
        options = get_user_instr(
            f"What would you like to {messages.underline('take')}?", player
        )
        if options is None:
            continue

        option, args = options
        if option == 'take':
            if args[0] == 'all':
                # don't want to affect loop by removing treasure from items
                for treasure in list(items):
                    try:
                        player.pick_up_item(treasure)
                        print(f"You picked up {treasure.name}!")
                    except InventoryFullException as e:
                        print(e)
                    else:
                        items.remove(treasure)

            elif args[0] == 'none':
                break
            else:
                try:
                    item_num = int(args[0])
                except ValueError:
                    print("take must be followed by a number")
                    continue
                if item_num > len(items) or item_num <= 0:
                    print(f"Invalid item number: {item_num}")
                    continue
                treasure = items[item_num - 1]
                try:
                    player.pick_up_item(treasure)
                    print(f"You picked up {treasure.name}!")
                except InventoryFullException as e:
                    print(e)
                else:
                    items.remove(treasure)

        if len(items) > 0:
            message = (
                f"Continue to take [{messages.underline('yes')}/"
                f"{messages.underline('no')}]?"
            )
            while (inputs := get_user_instr(message, player)) is None:
                continue
            if inputs[0] == 'no':
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
          "What would you like to take?")

    take_loop(player, chest.contents)


def retreat(player: Player):
    """
    Causes the Player to retreat to their previous room.

    This may be used instead of Player.retreat when it is desired that the game
    treats this movement as a re-entry of the room, including printing the
    room's description.

    """
    messages.print_enter(player.previous_room)
    player.retreat()


def attempt_sneak(player: Player, enemy: Enemy):
    """
    The Player attempts to sneak past an enemy.

    Success of the sneak attempt is determine by the player's luck statistic
    and a random element. If the attempt fails, a fight begins.

    """
    # If the player has the maximum luck value, there is a small chance
    # that their attempt will fail
    threshold = random.randint(0, constants.MAX_LUCK + 5)
    if player.get_luck() > threshold:
        # Success!
        print(f"You managed to slide past the {enemy.short_name} undetected!")
    else:
        # Failure...
        print("Oops... that didn't go to plan.")
        attack(player, enemy)


def trigger_trap(player: Player, trap: Trap) -> bool:
    """
    The player triggers the trap in room

    Whether the trap gets triggered is determine by the player's luck statistic
    and a random element. Once triggered, the trap will cause damage to player.

    """
    if trap.triggered:
        return False
    threshold = random.randint(0, constants.MAX_LUCK)
    if player.get_luck() >= threshold:
        # Safe!
        print(f"Phew...the {trap.name} wasn't triggered!")
        return False
    else:
        # Trap is triggered
        print("Oops...")
        time.sleep(2)
        print(f"{trap.description}. You lost {trap.damage} hp.")
        player.take_damage(trap.damage)
        player.move_to_new_room()
        trap.triggered = True
        return True
