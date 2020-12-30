from typing import List, Optional

from .character import Character
from .compass import Direction
from .item import Item
from .outfit import Outfit
from .room import Room
from .weapon import Weapon, WeaponBrokenException


class Player(Character):
    def __init__(
            self,
            name: str,
            hp: int,
            weapon: Optional[Weapon] = None,
            outfit: Optional[Outfit] = None
    ):
        super().__init__(name, hp)
        self.weapon = weapon
        self.outfit = outfit
        self.inventory: List[Item] = []
        self.previous_room: Optional[Room] = None
        self.current_room: Optional[Room] = None

    def move_to(self, room: Room):
        """
        Moves the Player to the target Room.

        Since this method is not relative to the Player's current location, it
        is only intended to be called from outside the class for initial
        placement of the Player. Internally, this condition is checked in
        Player.go, so this method may be used safely therein.

        Args:
            room: The Room to which the Player should be moved.

        """
        self.previous_room = self.current_room
        self.current_room = room

    def retreat(self):
        """
        Moves the Player to the previous Room.

        Note: If the previous Room is uninitialized, the behavior of this method
        is undefined.

        """
        self.move_to(self.previous_room)

    def go(self, direction: Direction):
        """
        Moves the Player in the target direction.

        This implementation assumes that external checks guarantee that the
        destination direction contains a Room. If this assumption does not hold,
        a NoSuchExitException will be raised.

        Args:
            direction: The Direction in which the Player should move.

        """
        if direction == Direction.North:
            self.move_to(self.current_room.north)
        elif direction == Direction.South:
            self.move_to(self.current_room.south)
        elif direction == Direction.East:
            self.move_to(self.current_room.east)
        else:
            self.move_to(self.current_room.west)

    def pick_up_item(self, item: Item):
        """
        Pick up an item

        Args:
            item: The item that got picked up

        """
        self.inventory.append(item)

    def change_weapon(self, weapon: Weapon):
        """
        Change the equipped weapon

        Args:
            weapon: The weapon to change to (must be contained in inventory)

        """
        self.inventory.remove(weapon)
        self.inventory.append(self.weapon)
        self.weapon = weapon

    def change_outfit(self, outfit: Outfit):
        """
        Change the equipped outfit

        Args:
            outfit: The outfit to change to (must be contained in inventory)

        """
        self.inventory.remove(outfit)
        self.inventory.append(self.outfit)
        self.outfit = outfit

    def attack(self, target: Character):
        """
        Attack the target character

        Args:
            target: The Character to attack

        Raises:
            WeaponBrokenException

        """
        if self.weapon.is_broken():
            raise WeaponBrokenException()

        self.weapon.decrement_durability()
        if target.is_alive():
            target.take_damage(self.weapon.attack_strength)

    def get_luck(self) -> int:
        """
        Get luck stats for Player

        Returns:
            Total number of luck points added from equipped weapon & outfit

        """
        return self.weapon.luck_stat + self.outfit.luck_stat
