import unittest

from adventure_game.enemy import Enemy, generate_enemy
from adventure_game import item
from adventure_game.outfit import Outfit
from adventure_game.player import Player
from adventure_game.weapon import Weapon


class EnemyGeneratorTests(unittest.TestCase):
    def test_basic_enemy(self):
        enemy = generate_enemy()
        self.assertIsInstance(enemy, Enemy)


class EnemyAttackTests(unittest.TestCase):
    def test_attack_player(self):
        e_weapon = Weapon("sword", 0, item.Rarity.Crappy, 3, 5)
        player = Player("tester", 10, None, None)
        enemy = Enemy("tester", "tester", 50, e_weapon)

        # Without outfit, the player will take all the damage (3) caused by e_weapon
        enemy.attack(player)
        self.assertEqual(player.hp, 7)

        # Wearing the outfit with 2 defence stat, the player will only take 1 damage this time
        p_outfit1 = Outfit("lan qipao", 0, item.Rarity.Common, 2)
        player.pick_up_item(p_outfit1)
        player.change_item("outfit", p_outfit1)
        enemy.attack(player)
        self.assertEqual(player.hp, 6)

        # Wearing the outfit with 4 defence stat, the player is immune from e_weapon
        p_outfit2 = Outfit("lan qipao", 0, item.Rarity.Super, 4)
        player.pick_up_item(p_outfit2)
        player.change_item("outfit", p_outfit2)
        enemy.attack(player)
        self.assertEqual(player.hp, 6)
