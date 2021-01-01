import unittest

from adventure_game.compass import (
    Direction, get_opposite_dir
)


class DirectionTests(unittest.TestCase):
    def test_opposite_dir(self):
        self.assertEqual(get_opposite_dir(Direction.North), Direction.South)
        self.assertEqual(get_opposite_dir(Direction.South), Direction.North)
        self.assertEqual(get_opposite_dir(Direction.East), Direction.West)
        self.assertEqual(get_opposite_dir(Direction.West), Direction.East)
