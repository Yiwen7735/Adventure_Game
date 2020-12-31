import unittest

from adventure_game.item import Rarity
from adventure_game.weapon import Weapon, generate_weapon


class WeaponTests(unittest.TestCase):
    def test_weapon_deterioration(self):
        weapon = Weapon("sword", 5, Rarity.Crappy, 5, 2)
        self.assertEqual(weapon.durability, 2)
        self.assertEqual(weapon.is_broken(), False)
        weapon.decrement_durability()
        self.assertEqual(weapon.durability, 1)
        self.assertEqual(weapon.is_broken(), False)
        weapon.decrement_durability()
        self.assertEqual(weapon.durability, 0)
        self.assertEqual(weapon.is_broken(), True)
        weapon.decrement_durability()
        self.assertEqual(weapon.durability, 0)
        self.assertEqual(weapon.is_broken(), True)


class WeaponGenerationTests(unittest.TestCase):
    def test_basic(self):
        weapon = generate_weapon()
        self.assertIsInstance(weapon, Weapon)
