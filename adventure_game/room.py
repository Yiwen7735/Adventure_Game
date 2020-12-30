"""
This module contains classes and functions to work with rooms in the
adventure game.

"""
from __future__ import annotations
import abc
import json
import random
from typing import Callable, Dict, List, Optional, TYPE_CHECKING

from . import compass, constants, enemy
from .chest import Chest
if TYPE_CHECKING:
    from .player import Player
from .trap import Trap
from .weapon import Weapon
from . import action

# Populate a set of descriptions from the predefined JSON
# These descriptions are used when dynamically generating new rooms
with open(constants.DATA_BANK_FILE) as fh:
    DESCRIPTION_BANK = json.load(fh)['room_descriptions']


class NoSuchExitException(Exception):
    """
    A basic exception type to be raised if the caller tries to travel in
    a direction which does not have a room.

    Note: this situation should only occur as a result of a programmer error.

    """
    pass


class Room(abc.ABC):
    """
    An abstract class used as the base class for all concrete implements of the
    Room type.

    Note: An abstract static method, generate, exists on all subclasses to
    randomly populate the room's description, and other fields as appropriate
    for the room type.

    Args:
        description: A player-facing description of the room.
        exits: A list of the directions in which the player can travel.
        weapon: An optional weapon lying on the room's floor.
        trap: An optional hidden trap in the room.

    """
    def __init__(
            self,
            description: str,
            exits: List[compass.Direction],
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.description = description
        self.weapon = weapon
        self.trap = trap

        self.exits = exits
        self._exits: Dict[compass.Direction, Optional[Room]] = {
            compass.Direction.North: None,
            compass.Direction.South: None,
            compass.Direction.East: None,
            compass.Direction.West: None,
        }

    @abc.abstractmethod
    def __str__(self):
        """
        Returns the player-facing description of the room.

        Note that this is abstract since concrete subclasses are expected to
        customize the format according to their room state.

        """
        pass

    @staticmethod
    @abc.abstractmethod
    def generate(exits: List[compass.Direction]) -> Room:
        """
        Dynamically generates an instance of the Room subclass.

        This method is expected to randomly initialize relevant fields of the
        subclass for use in map generation.

        """
        pass

    def get_exits(self) -> List[str]:
        """
        Returns a list of the string names of the directions in which the
        player can move.

        """
        return [d.name for d in self.exits]

    def get_options(self) -> Dict[str, Callable[[Player], ...]]:
        """
        Returns a map of the available special actions for the room, along
        with a callback handler to implement the action.

        Note that it is intended, but not required, that subclasses override
        this method to provide their own state-dependent actions.

        """
        return {}

    def _get_exit_room(self, d: compass.Direction):
        """
        Provides lazy initialization of the connecting Rooms for which the
        direction is present in the list of possible 'exits'.

        If the Room in direction 'd' has already been generated, the existing
        Room is returned. This allows the player to backtrack through already
        visited Rooms.

        Args:
            d: The direction whose Room to (possibly) generate and return.

        Returns:
            The Room in direction 'd'.

        """
        if d in self.exits:
            room = self._exits[d]
            if room is not None:
                return room
            opp = compass.get_opposite_dir(d)
            room = _generate_room(enter_from=opp)
            # Set the "backwards" room to the current room
            setattr(room, opp.name.lower(), self)
            self._exits[d] = room
            return room
        # This should only ever be reached due to programmer error
        raise NoSuchExitException()

    @property
    def north(self) -> Room:
        """Gets the Room in the Northern direction."""
        return self._get_exit_room(compass.Direction.North)

    @north.setter
    def north(self, v: Room):
        """Sets the Room in the Northern direction."""
        self._exits[compass.Direction.North] = v

    @property
    def south(self) -> Room:
        """Gets the Room in the Southern direction."""
        return self._get_exit_room(compass.Direction.South)

    @south.setter
    def south(self, v: Room):
        """Sets the Room in the Southern direction."""
        self._exits[compass.Direction.South] = v

    @property
    def east(self) -> Room:
        """Gets the Room in the Eastern direction."""
        return self._get_exit_room(compass.Direction.East)

    @east.setter
    def east(self, v: Room):
        """Sets the Room in the Eastern direction."""
        self._exits[compass.Direction.East] = v

    @property
    def west(self) -> Room:
        """Gets the Room in the Western direction."""
        return self._get_exit_room(compass.Direction.West)

    @west.setter
    def west(self, v: Room):
        """Sets the Room in the Western direction."""
        self._exits[compass.Direction.West] = v

    def has_trap(self) -> bool:
        """Checks whether the room contains a Trap"""
        return self.trap is not None


class EmptyRoom(Room):
    """A minimal room with no special actions available."""
    def __str__(self):
        return self.description

    @staticmethod
    def generate(exits: List[compass.Direction]) -> Room:
        """
        Produces a dynamically-generated empty room, with a description
        randomly selected from the bank.

        Returns:
            EmptyRoom

        """
        return EmptyRoom(random.choice(DESCRIPTION_BANK), exits)


class MonsterRoom(Room):
    """
    A special room containing an enemy to fight.

    Args:
        description: A player-facing description of the room.
        exits: A list of the directions in which the player can travel.
        monster: An Enemy to be optionally fought by the player.
        weapon: An optional weapon lying on the room's floor.
        trap: An optional hidden trap in the room.

    """
    def __init__(
            self,
            description: str,
            exits: List[compass.Direction],
            monster: enemy.Enemy,
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.monster = monster
        super().__init__(description, exits, weapon=weapon, trap=trap)

    def __str__(self):
        return f'{self.description}, with a {self.monster.name}'

    @staticmethod
    def generate(exits: List[compass.Direction]) -> Room:
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

    def get_options(self) -> Dict[str, Callable[[Player], ...]]:
        """
        Determines the special actions available, given the MonsterRoom's
        current state.

        In practice, this means that the options, if the monster is alive,
        are:
        1. Attack
        2. Flee to the previous room
        If the monster is dead, there are no special actions to be taken.

        Returns:
            Dictionary mapping action descriptions to callback handlers.

        """
        if self.monster.is_alive():
            action_handler = {
                f"Attack {self.monster.name}":
                    lambda player: action.attack(player, self.monster),
                "Run back": lambda player: player.retreat()
            }
            return action_handler
        return {}


class TreasureRoom(Room):
    def __init__(
            self,
            description: str,
            exits: List[compass.Direction],
            weapon: Optional[Weapon] = None,
            trap: Optional[Trap] = None
    ):
        self.chest = Chest()
        super().__init__(description, exits, weapon=weapon, trap=trap)

    def __str__(self):
        return f'{self.description}. An enticing chest sits in the centre'

    @staticmethod
    def generate(exits: List[compass.Direction]) -> Room:
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

    def get_options(self) -> Dict[str, Callable[[Player], ...]]:
        """
        Determines the special actions available, given the TreasureRoom's
        current state.

        In practice, this means that the options, if the monster is unopened,
        are:
        1. Open the chest and discover its contents
        2. Leave the chest alone
        If the chest has already been opened, there are no special actions
        available.

        Returns:
            Dictionary mapping action descriptions to callback handlers.

        """
        if self.chest.is_open:
            return {}

        action_handler = {
            "Open the chest": lambda player: action.collect(player, self.chest),
            "Leave it alone": lambda player: None
        }
        return action_handler


def _generate_room(enter_from: Optional[compass.Direction] = None) -> Room:
    """
    Produces a dynamically-generated room from the available room types,
    including a random set of possible exits.

    Note: this is only used in the Room class' implementation of the
    next room (north, south, east, west) 'pointers'.

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


def generate_first_room() -> Room:
    """
    Generates the first room of the level.

    Returns:
        Room

    """
    return EmptyRoom.generate(compass.DIRECTIONS)
