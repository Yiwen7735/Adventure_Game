import unittest

from adventure_game.character import Character


class CharacterTests(unittest.TestCase):
    def test_initial_is_alive(self):
        character = Character("Boy", 20)
        self.assertEqual(character.is_alive(), True)

    def test_initial_not_alive(self):
        character = Character("Boy", 0)
        self.assertEqual(character.hp, 0)
        self.assertEqual(character.is_alive(), False)

    def test_damaged_not_alive(self):
        character = Character("Boy", 10)
        character.take_damage(20)
        self.assertEqual(character.hp, 0)
        self.assertEqual(character.is_alive(), False)

    def test_damaged_still_alive(self):
        character = Character("Girl", 20)
        character.take_damage(19)
        self.assertEqual(character.hp, 1)
        self.assertEqual(character.is_alive(), True)
