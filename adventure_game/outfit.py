from . import item
import enum


class Outfit(item.Item):
    def __init__(self, name: str, luck_stat: int,
                 outfit_type: enum, defenses: int):
        super().__init__(name, luck_stat)
        self.outfit_type = outfit_type
        self.defenses = defenses


def generate_outfit() -> Outfit:
    pass
