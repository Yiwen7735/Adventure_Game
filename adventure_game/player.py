from typing import Optional

from .character import Character
from .weapon import Weapon, WeaponBrokenException
from .outfit import Outfit
from .item import Item


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
        self.inventory = []

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
