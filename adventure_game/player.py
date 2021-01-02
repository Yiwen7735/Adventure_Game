from typing import Dict, List, Optional

from .character import Character
from .compass import Direction
from .item import EquipmentItem, Item
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
        self.equipped: Dict[str, Optional[EquipmentItem]] = {
            "weapon": weapon,
            "outfit": outfit
        }
        self.inventory: Dict[str, List[Item]] = {
            "weapon": [],
            "outfit": []
        }
        self.previous_room: Optional[Room] = None
        self.current_room: Optional[Room] = None

    def __str__(self):
        weapon = self.equipped['weapon']
        outfit = self.equipped['outfit']
        return f"{self.name}: hp {self.hp}, " \
               f"holding {'Nothing' if weapon is None else weapon}, " \
               f"wearing {'Nothing' if outfit is None else outfit}"

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

        Note: If the previous Room is uninitialized, the behavior of this
        method is undefined.

        """
        self.move_to(self.previous_room)

    def go(self, direction: Direction):
        """
        Moves the Player in the target direction.

        Args:
            direction: The Direction in which the Player should move.

        Raises:
            NoSuchExitException: if the player attempts to move in a
                                 direction that does not have a room.

        """
        if self.current_room is not None:
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
        key = "weapon" if isinstance(item, Weapon) else "outfit"
        item_list = self.inventory[key]
        item_list.append(item)
        self.inventory[key] = item_list

    def equip(self, key: str, option: int):
        """
        Change the equipped item

        Args:
            key: The key referring to the type of item
            option: The option_th item in the inventory list

        """
        item = self.inventory[key][option - 1]
        self.change_item(key, item)

    def change_item(self, key: str, item: EquipmentItem):
        """
        Change the equipped item

        Args:
            key: The key referring to the type of item
            item: The item to change to (must be contained in inventory list)

        """
        item_list = self.inventory[key]
        item_list.remove(item)
        if self.equipped[key] is not None:
            item_list.append(self.equipped[key])
        self.inventory[key] = item_list
        self.equipped[key] = item

    def attack(self, target: Character):
        """
        Attack the target character

        Args:
            target: The Character to attack

        Raises:
            WeaponBrokenException

        """
        if self.equipped["weapon"] is None:
            damage = 1
        else:
            if self.equipped["weapon"].is_broken():
                raise WeaponBrokenException()
            damage = self.equipped["weapon"].attack_strength
            self.equipped["weapon"].decrement_durability()

        if target.is_alive():
            target.take_damage(damage)

    def get_luck(self) -> int:
        """
        Get luck stats for Player

        Returns:
            Total number of luck points added from equipped weapon & outfit

        """
        return sum([item.luck_stat for item in list(self.equipped.values())
                    if item is not None])
