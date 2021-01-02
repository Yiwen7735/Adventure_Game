import json
import random

from . import constants, item


class WeaponBrokenException(Exception):
    pass


class Weapon(item.EquipmentItem):
    def __init__(
            self,
            name: str,
            luck_stat: int,
            rarity: item.Rarity,
            attack_strength: int,
            durability: int
    ):
        super().__init__(name, luck_stat)
        self.rarity = rarity
        self.attack_strength = attack_strength
        self.durability = durability

    def __str__(self):
        """Returns the string representation of the Weapon."""
        return (f'{self.name} [attack: {self.attack_strength}, '
                f'durability: {self.durability}, luck: {self.luck_stat}]')

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
    rarity = random.choices(item.RARITIES, weights=[10, 5, 1])[0]
    rarity_str = rarity.name
    return Weapon(
        f"{rarity_str} {base['name']}",
        base["luck"][rarity_str],
        rarity,
        base["damage"][rarity_str],
        base["durability"][rarity_str]
    )
