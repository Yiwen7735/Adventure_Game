import enum


class Item:
    def __init__(self, name: str, luck_stat: int):
        self.name = name
        self.luck_stat = luck_stat


class Rarity(enum.Enum):
    Crappy = enum.auto()
    Common = enum.auto()
    Super = enum.auto()


RARITIES = [r for r in Rarity]
