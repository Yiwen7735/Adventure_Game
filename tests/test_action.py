import unittest

from adventure_game import action
from adventure_game.player import Player
from adventure_game.enemy import Enemy
from adventure_game.weapon import Weapon, WeaponType
from adventure_game.outfit import Outfit, OutfitType
from adventure_game.item import Item


class AttackTests(unittest.TestCase):
    pass
    """
    def test_attack(self):
        player = Player(
            "WeakDan",
            50,
            Weapon("sword", 0, WeaponType.Crappy, 10, 10),
            Outfit("slave clothes", 0, OutfitType.Crappy, 10)
        )

        monster = Enemy(
            "StrongZhu",
            100,
            Weapon("gun", 100, WeaponType.Super, 20, 20),
            Outfit("lan qipao", 0, OutfitType.Super, 50)
        )
        self.assertEqual(True, False)
    """

