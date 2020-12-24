from . import item
import enum


class OutfitType(enum.Enum):
    Crappy = enum.auto()
    Solid = enum.auto()
    Super = enum.auto()


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


def generate_outfit() -> Outfit:
    pass
