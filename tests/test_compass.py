import random
import unittest

from adventure_game.compass import (
    Direction, get_opposite_dir, get_random_directions
)


class DirectionTests(unittest.TestCase):
    def test_opposite_dir(self):
        self.assertEqual(get_opposite_dir(Direction.North), Direction.South)
        self.assertEqual(get_opposite_dir(Direction.South), Direction.North)
        self.assertEqual(get_opposite_dir(Direction.East), Direction.West)
        self.assertEqual(get_opposite_dir(Direction.West), Direction.East)

    def test_get_random_directions(self):
        random.seed(1)
        for _ in range(100):
            dirs = get_random_directions()
            # Check for duplicates - there shouldn't be any
            self.assertEqual(len(dirs), len(set(dirs)))
