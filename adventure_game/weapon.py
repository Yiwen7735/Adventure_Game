from . import item
import enum


class WeaponType(enum.Enum):
    Crappy = enum.auto()
    Solid = enum.auto()
    Super = enum.auto()


class WeaponBrokenException(Exception):
    pass


class Weapon(item.Item):
    def __init__(
            self,
            name: str,
            luck_stat: int,
            weapon_type: WeaponType,
            attack_strength: int,
            durability: int
    ):
        super().__init__(name, luck_stat)
        self.weapon_type = weapon_type
        self.attack_strength = attack_strength
        self.durability = durability

    def decrement_durability(self):
        """
        Decrement the weapon's durability by 1

        """
        if self.durability > 0:
            self.durability -= 1

    def is_broken(self) -> bool:
        """
        Check if the weapon is broken

        Returns:
            true if durability is 0 and false otherwise

        """
        return self.durability == 0


def generate_weapon() -> Weapon:
    pass
