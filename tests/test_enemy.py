import unittest

from adventure_game.enemy import Enemy, generate_enemy


class EnemyGeneratorTests(unittest.TestCase):
    def test_basic_enemy(self):
        enemy = generate_enemy()
        self.assertIsInstance(enemy, Enemy)
