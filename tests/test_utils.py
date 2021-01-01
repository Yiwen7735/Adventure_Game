import unittest

from adventure_game.compass import Direction
from adventure_game.utils import parse_movement_instr


class ParseMovementTests(unittest.TestCase):
    def test_parse_all_correct_cases(self):
        for direction in ['north', 'south', 'east', 'west']:
            with self.subTest(direction=direction):
                d = Direction[direction.capitalize()]
                self.assertEqual(
                    parse_movement_instr(f'go {direction}'),
                    d
                )
                self.assertEqual(
                    parse_movement_instr(f'go {direction.capitalize()}'),
                    d
                )
                self.assertEqual(
                    parse_movement_instr(f'go {direction.upper()}'),
                    d
                )

    def test_parse_no_go(self):
        self.assertIsNone(parse_movement_instr('move north'))

    def test_parse_direction_typo(self):
        self.assertIsNone(parse_movement_instr('go nrth'))
