"""
This module contains classes and functions to work with rooms in the
adventure game.

"""
import abc
from typing import List, Optional

from .item import Item
from .enemy import Enemy
from .trap import Trap
from .weapon import Weapon


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


class EmptyRoom(Room):
    def __str__(self):
        return self.description


class MonsterRoom(Room):
    def __init__(
            self,
            description: str,
            enemy: Enemy,
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.monster = enemy
        super().__init__(description, weapon, trap)

    def __str__(self):
        return f"{self.description}, with a {self.monster.name}"


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
        return f"{self.description}. An enticing chest sits in the centre"

    def open_chest(self) -> List[Item]:
        """
        Reveals the treasure hidden in the room's chest.

        Returns:
            List of contained Items.

        """
        return self.treasure
