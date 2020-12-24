from .character import Character
from .player import Player
from .weapon import Weapon


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
