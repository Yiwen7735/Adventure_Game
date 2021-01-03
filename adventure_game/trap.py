import json
import random

from . import constants


class Trap:
    def __init__(self,
                 name: str,
                 description: str,
                 damage: int):
        self.name = name
        self.description = description
        self.damage = damage


with open(constants.DATA_BANK_FILE) as fh:
    TRAP_DATA_BANK = json.load(fh)["trap"]


def generate_trap() -> Trap:
    trap = random.choice(TRAP_DATA_BANK)
    return Trap(
        trap["name"],
        trap["description"],
        trap["damage"]
    )
