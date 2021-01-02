import enum


class Item:
    """
    This class is an abstract class intended to be inherited by all items
    in the game, including equipment (weapons/outfits) and food.

    Args:
        name: The name of the item.

    """
    def __init__(self, name: str):
        self.name = name


class EquipmentItem(Item):
    """
    An abstract class intended to be inherited by all 'equippable' items in
    the game, meaning the Player's (or Enemy's) equipment.

    Args:
        name: The name of the item.
        luck_stat: The luck value associated with the item.

    """
    def __init__(self, name: str, luck_stat: int):
        super().__init__(name)
        self.luck_stat = luck_stat


class FoodItem(Item):
    """
    An class representing food items which restore a certain amount of health
    to the player when consumed.

    Args:
        name: The name of the item.
        restore_amount: The amount of health points gained when the food is
                        consumed.

    """
    def __init__(self, name: str, restore_amount: int):
        super().__init__(name)
        self.restore_amount = restore_amount


class Rarity(enum.Enum):
    Crappy = enum.auto()
    Common = enum.auto()
    Super = enum.auto()


RARITIES = [r for r in Rarity]
