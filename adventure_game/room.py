"""
This module contains classes and functions to work with rooms in the
adventure game.

"""
import abc
import json
import random
from typing import List, Optional

from . import constants, enemy, outfit
from .item import Item
from .trap import Trap
from .weapon import Weapon, generate_weapon


with open(constants.DATA_BANK_FILE) as fh:
    DESCRIPTION_BANK = json.load(fh)['room_descriptions']


class Room(abc.ABC):
    def __init__(
            self,
            description: str,
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.description = description
        self.weapon = weapon
        self.trap = trap

        self.north: Optional[Room] = None
        self.south: Optional[Room] = None
        self.east: Optional[Room] = None
        self.west: Optional[Room] = None

    @abc.abstractmethod
    def __str__(self):
        pass

    def has_trap(self) -> bool:
        """Checks whether the room contains a Trap"""
        return self.trap is not None


class EmptyRoom(Room):
    def __str__(self):
        return self.description


class MonsterRoom(Room):
    def __init__(
            self,
            description: str,
            monster: enemy.Enemy,
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.monster = monster
        super().__init__(description, weapon, trap)

    def __str__(self):
        return f'{self.description}, with a {self.monster.name}'


class TreasureRoom(Room):
    def __init__(
            self,
            description: str,
            items: List[Item],
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.treasure = items
        super().__init__(description, weapon, trap)

    def __str__(self):
        return f'{self.description}. An enticing chest sits in the centre'

    def open_chest(self) -> List[Item]:
        """
        Reveals the treasure hidden in the room's chest.

        Returns:
            List of contained Items.

        """
        return self.treasure


def generate_empty_room() -> EmptyRoom:
    """
    Produces a dynamically-generated empty room, with a description
    randomly selected from the bank.

    Returns:
        EmptyRoom

    """
    return EmptyRoom(random.choice(DESCRIPTION_BANK))


def generate_monster_room() -> MonsterRoom:
    """
    Produces a dynamically-generated room containing an enemy.

    The description is randomly selected from the bank, while a monster
    is generated from the available features.

    Returns:
        MonsterRoom

    """
    return MonsterRoom(
        random.choice(DESCRIPTION_BANK),
        enemy.generate_enemy()
    )


def generate_treasure() -> List[Item]:
    """
    Generates a list of items to be served as treasure to the player.

    Returns:
        List of Items

    """
    n = random.randint(1, 3)
    items: List[Item] = []
    for _ in range(n):
        if random.randint(0, 1) == 0:
            # Weapon
            items.append(generate_weapon())
        else:
            # Outfit
            items.append(outfit.generate_outfit())
    return items


def generate_treasure_room() -> TreasureRoom:
    """
    Produces a dynamically-generated room containing treasure.

    The description is randomly selected from the bank, while a random
    amount of treasure is also randomly generated.

    Returns:
        TreasureRoom

    """
    return TreasureRoom(
        random.choice(DESCRIPTION_BANK),
        generate_treasure()
    )
