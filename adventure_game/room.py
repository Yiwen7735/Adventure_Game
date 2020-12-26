"""
This module contains classes and functions to work with rooms in the
adventure game.

"""
import abc
import json
import random
from typing import Dict, List, Optional

from . import compass, constants, enemy
from .chest import Chest
from .trap import Trap
from .weapon import Weapon


with open(constants.DATA_BANK_FILE) as fh:
    DESCRIPTION_BANK = json.load(fh)['room_descriptions']


class NoSuchExitException(Exception):
    pass


class Room(abc.ABC):
    def __init__(
            self,
            description: str,
            open_exits: List[compass.Direction],
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.description = description
        self.weapon = weapon
        self.trap = trap

        self.open_exits = open_exits
        self._exits: Dict[compass.Direction, Optional[Room]] = {
            compass.Direction.North: None,
            compass.Direction.South: None,
            compass.Direction.East: None,
            compass.Direction.West: None,
        }

    @abc.abstractmethod
    def __str__(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def generate(exits: List[compass.Direction]) -> "Room":
        pass

    def get_options(self):
        return []

    def _get_exit_room(self, d: compass.Direction):
        """
        Provides lazy initialization of the connecting Rooms.

        """
        if d in self.open_exits:
            room = self._exits[d]
            if room is not None:
                return room
            opp = compass.get_opposite_dir(d)
            room = generate_room(enter_from=opp)
            setattr(room, opp.name.lower(), self)
            self._exits[d] = room
            return room
        raise NoSuchExitException()

    @property
    def north(self) -> "Room":
        return self._get_exit_room(compass.Direction.North)

    @north.setter
    def north(self, v: "Room"):
        self._exits[compass.Direction.North] = v

    @property
    def south(self) -> "Room":
        return self._get_exit_room(compass.Direction.South)

    @south.setter
    def south(self, v: "Room"):
        self._exits[compass.Direction.South] = v

    @property
    def east(self) -> "Room":
        return self._get_exit_room(compass.Direction.East)

    @east.setter
    def east(self, v: "Room"):
        self._exits[compass.Direction.East] = v

    @property
    def west(self) -> "Room":
        return self._get_exit_room(compass.Direction.West)

    @west.setter
    def west(self, v: "Room"):
        self._exits[compass.Direction.West] = v

    def has_trap(self) -> bool:
        """Checks whether the room contains a Trap"""
        return self.trap is not None


class EmptyRoom(Room):
    def __str__(self):
        return self.description

    @staticmethod
    def generate(exits: List[compass.Direction]) -> "Room":
        """
        Produces a dynamically-generated empty room, with a description
        randomly selected from the bank.

        Returns:
            EmptyRoom

        """
        return EmptyRoom(random.choice(DESCRIPTION_BANK), exits)


class MonsterRoom(Room):
    def __init__(
            self,
            description: str,
            open_exits: List[compass.Direction],
            monster: enemy.Enemy,
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.monster = monster
        super().__init__(description, open_exits, weapon=weapon, trap=trap)

    def __str__(self):
        return f'{self.description}, with a {self.monster.name}'

    @staticmethod
    def generate(exits: List[compass.Direction]) -> "Room":
        """
            Produces a dynamically-generated room containing an enemy.

            The description is randomly selected from the bank, while a monster
            is generated from the available features.

            Returns:
                MonsterRoom

            """
        return MonsterRoom(
            random.choice(DESCRIPTION_BANK),
            exits,
            enemy.generate_enemy()
        )

    def get_options(self):
        if self.monster.is_alive():
            action_handler = {
                f"Attack {self.monster.name}": lambda player: player.attack(self.monster),
                "Run back": lambda player: player.retreat()}
            return action_handler
        return {}


class TreasureRoom(Room):
    def __init__(
            self,
            description: str,
            open_exits: List[compass.Direction],
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.chest = Chest()
        super().__init__(description, open_exits, weapon=weapon, trap=trap)

    def __str__(self):
        return f'{self.description}. An enticing chest sits in the centre'

    @staticmethod
    def generate(exits: List[compass.Direction]) -> "Room":
        """
            Produces a dynamically-generated room containing treasure.

            The description is randomly selected from the bank, while a random
            amount of treasure is also randomly generated.

            Returns:
                TreasureRoom

            """
        return TreasureRoom(
            random.choice(DESCRIPTION_BANK),
            exits
        )

    def get_options(self):
        if self.chest.is_open:
            return {}

        action_handler = {
            "Open the chest": lambda player: self.chest.open(),
            "Leave it alone": lambda player: None}
        return action_handler


def generate_room(enter_from: Optional[compass.Direction] = None) -> Room:
    """
    Produces a dynamically-generated room from the available room types,
    including a random set of possible exits.

    Returns:
        Room

    """
    exits = compass.get_random_directions()
    if enter_from is not None and enter_from not in exits:
        exits.append(enter_from)

    room_type = random.randint(1, 3)
    if room_type == 1:
        return EmptyRoom.generate(exits)
    elif room_type == 2:
        return MonsterRoom.generate(exits)
    return TreasureRoom.generate(exits)

