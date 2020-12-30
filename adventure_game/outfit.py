import enum
import json
import random

from . import constants, item


class OutfitType(enum.Enum):
    Crappy = enum.auto()
    Solid = enum.auto()
    Super = enum.auto()


OUTFIT_TYPES = [t for t in OutfitType]


class Outfit(item.Item):
    def __init__(
            self,
            name: str,
            luck_stat: int,
            outfit_type: OutfitType,
            defence: int
    ):
        super().__init__(name, luck_stat)
        self.outfit_type = outfit_type
        self.defence = defence


with open(constants.DATA_BANK_FILE) as fh:
    OUTFIT_TYPE_BANK = json.load(fh)['outfit_types']


def generate_outfit() -> Outfit:
    base = random.choice(OUTFIT_TYPE_BANK)
    level = random.choices(OUTFIT_TYPES, weights=[10, 5, 1])[0]
    level_str = level.name
    return Outfit(
        f"{level.name} {base['name']}",
        base["luck"][level_str],
        level,
        base["defence"][level_str]
    )
