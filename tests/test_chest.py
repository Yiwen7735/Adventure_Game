import unittest
from unittest.mock import patch

from adventure_game.chest import Chest


class ChestTests(unittest.TestCase):
    def test_full_chest_remove_one_by_one(self):
        chest = Chest()
        self.assertEqual(chest.is_open, False)
        with patch('adventure_game.chest.random.randint', lambda a, b: 3):
            chest.open()
        self.assertEqual(chest.is_open, True)

        self.assertEqual(len(chest.contents), 3)
        for i, item in enumerate(chest.contents):
            chest.remove(item)
            self.assertEqual(len(chest.contents), 3 - i - 1)

    def test_full_chest_take_all(self):
        chest = Chest()
        with patch('adventure_game.chest.random.randint', lambda a, b: 3):
            chest.open()

        self.assertEqual(len(chest.contents), 3)
        chest.clear()
        self.assertEqual(len(chest.contents), 0)

    def test_chest_can_only_be_opened_once(self):
        chest = Chest()
        with patch('adventure_game.chest.random.randint', lambda a, b: 3):
            chest.open()
            chest.open()

        self.assertEqual(len(chest.contents), 3)

    def test_empty_chest(self):
        chest = Chest()
        with patch('adventure_game.chest.random.randint', lambda a, b: 0):
            chest.open()

        self.assertEqual(len(chest.contents), 0)

    def test_remove_already_removed_item(self):
        chest = Chest()
        with patch('adventure_game.chest.random.randint', lambda a, b: 1):
            chest.open()

        self.assertEqual(len(chest.contents), 1)
        item = chest.contents[0]
        chest.remove(item)
        self.assertEqual(len(chest.contents), 0)
        chest.remove(item)
        self.assertEqual(len(chest.contents), 0)
