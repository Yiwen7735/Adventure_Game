import random
from typing import List

from .item import Item
from .outfit import generate_outfit
from .weapon import generate_weapon


class Chest:
    def __init__(self):
        self.contents: List[Item] = []
        self.is_open = False

    def open(self) -> List[Item]:
        """
        Generates a list of items to be served as treasure to the player.

        Returns:
            List of Items

        """
        self.is_open = True
        n = random.randint(0, 3)
        for _ in range(n):
            if random.randint(0, 1) == 0:
                # Weapon
                self.contents.append(generate_weapon())
            else:
                # Outfit
                self.contents.append(generate_outfit())
        return self.contents

    def remove(self, item: Item):
        """
        Remove an item from the list
        Returns:

        """
        if item in self.contents:
            self.contents.remove(item)

    def clear(self):
        """
        Clear the chest (removing all items at once)

        """
        for item in self.contents:
            self.contents.remove(item)
