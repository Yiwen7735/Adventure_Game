import enum
import json
import random

from . import constants


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
        msg: A message to be output when the item is eaten by the player.

    """
    def __init__(self, name: str, restore_amount: int, msg: str):
        super().__init__(name)
        self.restore_amount = restore_amount
        self.consume_msg = msg

    def __str__(self):
        return f'{self.name}'


with open(constants.DATA_BANK_FILE) as fh:
    FOOD_BANK = json.load(fh)['food']


def generate_food() -> FoodItem:
    """Randomly generates a piece of food from the available options."""
    presets = random.choice(FOOD_BANK)
    return FoodItem(presets['name'], presets['hp'], presets['msg'])


class Rarity(enum.Enum):
    Crappy = enum.auto()
    Common = enum.auto()
    Super = enum.auto()


RARITIES = [r for r in Rarity]
