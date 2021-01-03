"""
This module contains classes and functions to work with rooms in the
adventure game.

"""
from __future__ import annotations
import abc
import json
import random
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from . import action, compass, constants, item, enemy, messages
from .chest import Chest
from .trap import Trap
from .weapon import generate_weapon
if TYPE_CHECKING:
    from .player import Player

# Populate a set of descriptions from the predefined JSON
# These descriptions are used when dynamically generating new rooms
with open(constants.DATA_BANK_FILE) as fh:
    DESCRIPTION_BANK = json.load(fh)['room_descriptions']


class NoSuchExitException(Exception):
    """
    A basic exception type to be raised if the caller tries to travel in
    a direction which does not have a room.

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
        items: An optional list of Items found in the room.
        trap: An optional hidden trap in the room.

    """
    def __init__(
            self,
            description: str,
            exits: List[compass.Direction],
            items: Optional[List[item.Item]] = None,
            trap: Optional[Trap] = None
    ):
        self.description = description
        self.items: List[item.Item] = items if items is not None else []
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

    def add_item(self, new_item: item.Item):
        """Adds a new item to the floor of the room."""
        self.items.append(new_item)

    def get_options(self) -> Dict[str, Callable[[Player], Any]]:
        """
        Returns a map of the available special actions for the room, along
        with a callback handler to implement the action.

        Note that it is intended, but not required, that subclasses override
        this method to provide their own state-dependent actions. They should
        each call this base class method to facilitate pick-up of dropped
        items or food.

        """
        options = {}
        if self.items:
            options['Look at items on the floor'] = \
                lambda player: action.take_loop(player, self.items)
            options['Ignore floor-based garbage'] = lambda _: None

        return options

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
    """
    A minimal room. Its sole special action is the possibility of their being
    a weapon lying on the floor, which the player may take.

    """
    def __str__(self):
        desc = self.description
        if self.items:
            desc += f". There is something lying on the floor"
        return desc

    @staticmethod
    def generate(exits: List[compass.Direction]) -> EmptyRoom:
        """
        Produces a dynamically-generated empty room, with a description
        randomly selected from the bank.

        Returns:
            EmptyRoom

        """
        items = []
        if random.randint(0, 1) == 1:
            # 50% chance that the room will include a weapon
            items.append(generate_weapon())
        if random.randint(0, 1) == 1:
            # 50% chance that the room will include a piece of food
            items.append(item.generate_food())
        return EmptyRoom(
            random.choice(DESCRIPTION_BANK),
            exits,
            items=items
        )


class MonsterRoom(Room):
    """
    A special room containing an enemy to fight.

    Args:
        description: A player-facing description of the room.
        exits: A list of the directions in which the player can travel.
        monster: An Enemy to be optionally fought by the player.
        trap: An optional hidden trap in the room.

    """
    def __init__(
            self,
            description: str,
            exits: List[compass.Direction],
            monster: enemy.Enemy,
            trap: Optional[Trap] = None
    ):
        self.monster = monster
        super().__init__(description, exits, trap=trap)

    def __str__(self):
        desc = f'{self.description}, with '
        if not self.monster.is_alive():
            desc += 'the corpse of '
        desc += f'{messages.get_a_or_an(self.monster.name)} {self.monster.name}'
        return desc

    @staticmethod
    def generate(exits: List[compass.Direction]) -> MonsterRoom:
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

    def get_options(self) -> Dict[str, Callable[[Player], Any]]:
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
                f"Attempt to sneak past the {self.monster.short_name}":
                    lambda player: action.attempt_sneak(player, self.monster),
                "Run back": action.retreat
            }
            return action_handler
        return super().get_options()


class TreasureRoom(Room):
    def __init__(
            self,
            description: str,
            exits: List[compass.Direction],
            trap: Optional[Trap] = None
    ):
        self.chest = Chest()
        super().__init__(description, exits, trap=trap)

    def __str__(self):
        desc = f'{self.description}. '
        if self.chest.is_open:
            desc += 'An open, empty'
        else:
            desc += 'An enticing'
        desc += ' sits in the centre'
        return desc

    @staticmethod
    def generate(exits: List[compass.Direction]) -> TreasureRoom:
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

    def get_options(self) -> Dict[str, Callable[[Player], Any]]:
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
            return super().get_options()

        action_handler = {
            "Open the chest":
                lambda player: action.collect(player, self.chest),
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
    # Select between 2 and 4 directions to have an exit - 1 is not an option
    # since it would allow for a "closed" maze to be formed
    exits = random.sample(compass.DIRECTIONS, random.randint(2, 4))
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
