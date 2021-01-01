import json
import random

from . import constants, item


class Outfit(item.Item):
    def __init__(
            self,
            name: str,
            luck_stat: int,
            rarity: item.Rarity,
            defence: int
    ):
        super().__init__(name, luck_stat)
        self.rarity = rarity
        self.defence = defence

    def __str__(self):
        """Returns the string representation of the Outfit."""
        return (f'{self.name} [defence: {self.defence}, '
                f'luck: {self.luck_stat}]')


with open(constants.DATA_BANK_FILE) as fh:
    OUTFIT_TYPE_BANK = json.load(fh)['outfit_types']


def generate_outfit() -> Outfit:
    base = random.choice(OUTFIT_TYPE_BANK)
    rarity = random.choices(item.RARITIES, weights=[10, 5, 1])[0]
    rarity_str = rarity.name
    return Outfit(
        f"{rarity_str} {base['name']}",
        base["luck"][rarity_str],
        rarity,
        base["defence"][rarity_str]
    )
