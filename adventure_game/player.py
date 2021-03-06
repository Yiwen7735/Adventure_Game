from typing import cast, Dict, List, Optional

from . import constants
from .character import Character
from .compass import Direction
from .exceptions import InventoryFullException, WeaponBrokenException
from .item import EquipmentItem, FoodItem, Item
from .outfit import Outfit
from .room import Room, generate_first_room
from .weapon import Weapon


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
            "outfit": [],
            "food": [],
        }
        self.previous_room: Optional[Room] = None
        self.current_room: Optional[Room] = None

    @property
    def cur_weapon(self) -> Weapon:
        return cast(Weapon, self.equipped["weapon"])

    @cur_weapon.setter
    def cur_weapon(self, weapon: Weapon):
        self.equipped["weapon"] = weapon

    @property
    def cur_outfit(self) -> Outfit:
        return cast(Outfit, self.equipped["outfit"])

    @cur_outfit.setter
    def cur_outfit(self, outfit: Outfit):
        self.equipped["outfit"] = outfit

    @property
    def weapons(self) -> List[Weapon]:
        return cast(List[Weapon], self.inventory["weapon"])

    @property
    def outfits(self) -> List[Outfit]:
        return cast(List[Outfit], self.inventory["outfit"])

    @property
    def foods(self) -> List[FoodItem]:
        return cast(List[FoodItem], self.inventory["food"])

    def __str__(self):
        weapon = self.cur_weapon
        outfit = self.cur_outfit
        return f"{self.name}: hp {self.hp}, " \
               f"holding {'Nothing' if weapon is None else weapon}, " \
               f"wearing {'Nothing' if outfit is None else outfit}"

    def move_to_new_room(self):
        new_room = generate_first_room()
        self.move_to(new_room)

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
        if isinstance(item, Weapon):
            if len(self.weapons) < constants.MAX_WEAPON:
                self.weapons.append(item)
            else:
                raise InventoryFullException("Your weapon pocket is full.")
        elif isinstance(item, Outfit):
            if len(self.outfits) < constants.MAX_OUTFIT:
                self.outfits.append(item)
            else:
                raise InventoryFullException("Your outfit pocket is full.")
        elif isinstance(item, FoodItem):
            if len(self.foods) < constants.MAX_FOOD:
                self.foods.append(item)
            else:
                raise InventoryFullException("Your food pocket is full.")

    def equip(self, key: str, option: int):
        """
        Change the equipped item

        Args:
            key: The key referring to the type of item
            option: The option_th item in the inventory list

        """
        item = self.inventory[key][option - 1]
        self.change_item(key, cast(EquipmentItem, item))

    def change_item(self, key: str, item: EquipmentItem):
        """
        Change the equipped item

        Args:
            key: The key referring to the type of item
            item: The item to change to (must be contained in inventory list)

        """
        self.inventory[key].remove(item)
        if self.equipped[key] is not None:
            self.inventory[key].append(self.equipped[key])
        self.equipped[key] = item

    def throw(self):
        """
        Throw away the weapon currently equipped
        """
        self.current_room.add_item(self.equipped["weapon"])
        self.cur_weapon = None

    def drop(self, key: str, option: int):
        """
        Drop an item from the inventory into the current room.

        Args:
            key: The key referring to the type of item
            option: The option_th item in the inventory list

        """
        drop_item = self.inventory[key][option - 1]
        self.inventory[key].remove(drop_item)
        self.current_room.add_item(drop_item)

    def eat(self, option: int):
        """
        Eats a piece of food from the inventory.

        Args:
            option: The option_th item in the food inventory list.

        """
        food = self.foods[option]
        self.heal(food.restore_amount)
        self.foods.remove(food)

    def attack(self, target: Character):
        """
        Attack the target character

        Args:
            target: The Character to attack

        Raises:
            WeaponBrokenException

        """
        if self.cur_weapon is None:
            damage = 1
        else:
            if self.cur_weapon.is_broken():
                raise WeaponBrokenException()
            damage = self.cur_weapon.attack_strength
            self.cur_weapon.decrement_durability()

        if target.is_alive():
            target.take_damage(damage)

    def get_luck(self) -> int:
        """
        Get luck stats for Player

        Returns:
            Total number of luck points added from equipped weapon & outfit

        """
        return min(
            constants.MAX_LUCK,
            sum([item.luck_stat for item in list(self.equipped.values())
                 if item is not None])
        )
