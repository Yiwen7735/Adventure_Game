import enum
import json
import random

from . import constants, item


class WeaponType(enum.Enum):
    Crappy = enum.auto()
    Solid = enum.auto()
    Super = enum.auto()


WEAPON_TYPES = [t for t in WeaponType]


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


with open(constants.DATA_BANK_FILE) as fh:
    WEAPON_TYPE_BANK = json.load(fh)['weapon_types']


def generate_weapon() -> Weapon:
    base = random.choice(WEAPON_TYPE_BANK)
    level = random.choices(WEAPON_TYPES, weights=[10, 5, 1])[0]
    level_str = level.name
    return Weapon(
        f"{level.name} {base['name']}",
        base["luck"][level_str],
        level,
        base["damage"][level_str],
        base["durability"][level_str]
    )
