import unittest

from adventure_game.enemy import Enemy
from adventure_game.player import Player
from adventure_game.outfit import Outfit, OutfitType
from adventure_game.weapon import Weapon, WeaponType


class PlayerTests(unittest.TestCase):
    def test_basic_player(self):
        player = Player(
            "Tester",
            100,
            Weapon("sword", 0, WeaponType.Crappy, 10, 10),
            Outfit("slave clothes", 0, OutfitType.Crappy, 10)
        )
        self.assertIsInstance(player, Player)

    def test_pick_up_item(self):
        player = Player(
            "Tester",
            100,
            Weapon("sword", 0, WeaponType.Crappy, 10, 10),
            Outfit("slave clothes", 0, OutfitType.Crappy, 10)
        )
        weapon = Weapon("axe", 0, WeaponType.Crappy, 5, 2)
        player.pick_up_item(weapon)
        self.assertTrue(weapon in player.inventory)

    def test_change_weapon(self):
        starting_weapon = Weapon("sword", 1, WeaponType.Crappy, 5, 5)
        player = Player(
            "Tester",
            100,
            starting_weapon,
            Outfit("pirate costume", 5, OutfitType.Solid, 5)
        )
        self.assertEqual(player.weapon, starting_weapon)
        weapon = Weapon("axe", 0, WeaponType.Solid, 10, 10)
        player.pick_up_item(weapon)
        self.assertEqual(player.weapon, starting_weapon)
        self.assertTrue(weapon in player.inventory)
        player.change_weapon(weapon)
        self.assertEqual(player.weapon, weapon)
        self.assertTrue(starting_weapon in player.inventory)

    def test_change_weapon_same_name(self):
        starting_weapon = Weapon("sword", 1, WeaponType.Crappy, 5, 5)
        player = Player(
            "Tester",
            100,
            starting_weapon,
            Outfit("pirate costume", 5, OutfitType.Solid, 5)
        )
        self.assertEqual(player.weapon, starting_weapon)
        weapon = Weapon("sword", 0, WeaponType.Solid, 10, 10)
        player.pick_up_item(weapon)
        self.assertEqual(player.weapon, starting_weapon)
        self.assertTrue(weapon in player.inventory)
        player.change_weapon(weapon)
        self.assertEqual(player.weapon, weapon)
        self.assertTrue(starting_weapon in player.inventory)

    def test_change_outfit(self):
        starting_outfit = Outfit("plain clothes", 0, OutfitType.Crappy, 1)
        player = Player(
            "Tester",
            100,
            Weapon("gun", 2, WeaponType.Super, 15, 15),
            starting_outfit
        )
        self.assertEqual(player.outfit, starting_outfit)
        outfit = Outfit("clown costume", 5, OutfitType.Solid, 10)
        player.pick_up_item(outfit)
        self.assertEqual(player.outfit, starting_outfit)
        self.assertTrue(outfit in player.inventory)
        player.change_outfit(outfit)
        self.assertEqual(player.outfit, outfit)
        self.assertTrue(starting_outfit in player.inventory)

    def test_change_outfit_same_name(self):
        starting_outfit = Outfit("plain clothes", 0, OutfitType.Crappy, 1)
        player = Player(
            "Tester",
            100,
            Weapon("gun", 2, WeaponType.Super, 15, 15),
            starting_outfit
        )
        self.assertEqual(player.outfit, starting_outfit)
        outfit = Outfit("plain_clothes", 5, OutfitType.Solid, 10)
        player.pick_up_item(outfit)
        self.assertEqual(player.outfit, starting_outfit)
        self.assertTrue(outfit in player.inventory)
        player.change_outfit(outfit)
        self.assertEqual(player.outfit, outfit)
        self.assertTrue(starting_outfit in player.inventory)

    def test_luck(self):
        weapon = Weapon("sword", 1, WeaponType.Solid, 5, 5)
        outfit = Outfit("beautiful dress", 10, OutfitType.Super, 15)
        player = Player(
            "Tester",
            100,
            weapon,
            outfit
        )
        self.assertEqual(player.get_luck(), weapon.luck_stat + outfit.luck_stat)

    def test_attack_enemy(self):
        weapon = Weapon("sword", 5, WeaponType.Solid, 5, 5)
        outfit = Outfit("qipao", 10, OutfitType.Super, 5)
        player = Player(
            "Tester",
            100,
            weapon,
            outfit
        )
        enemy = Enemy("beast", 10, Weapon("axe", 0, WeaponType.Crappy, 5, 10))
        player.attack(enemy)
        self.assertEqual(enemy.hp, 5)
        player.attack(enemy)
        self.assertEqual(enemy.hp, 0)
        player.attack(enemy)
        self.assertEqual(enemy.hp, 0)
