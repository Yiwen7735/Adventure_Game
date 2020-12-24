import json
import random

from . import constants
from .character import Character
from .player import Player
from .weapon import Weapon, generate_weapon


with open(constants.DATA_BANK_FILE) as fh:
    ENEMY_BANK = json.load(fh)['enemies']


class Enemy(Character):
    def __init__(self, name: str, hp: int, weapon: Weapon):
        self.weapon = weapon
        super().__init__(name, hp)

    def attack(self, target: Player):
        """
        Attack the target player.

        Args:
            target: The Player to attack.

        """
        if target.is_alive():
            target.take_damage(self.weapon.attack_strength)


def generate_enemy() -> Enemy:
    """
    Produces a dynamically-generated enemy.

    Returns:
        Enemy

    """
    presets = random.choice(ENEMY_BANK)
    weapon = generate_weapon()
    return Enemy(
        presets['name'],
        presets['hp'],
        weapon
    )
