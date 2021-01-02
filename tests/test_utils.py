import unittest
from unittest.mock import patch

from adventure_game import item
from adventure_game.compass import Direction
from adventure_game.outfit import Outfit
from adventure_game.player import Player
from adventure_game.utils import equip, parse_movement_instr


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


class EquipTests(unittest.TestCase):
    def test_equip_nonexistent_items(self):
        player = Player("Tester", 100, None, None)
        inputs = (i for i in ["w1", "o2", "o1"])

        def mock_input(*args):
            return next(inputs)

        with patch('builtins.input', mock_input):
            equip(player)

            # The player should not be able to equip non-existent items
            self.assertIsNone(player.equipped["weapon"])
            player.pick_up_item(Outfit("qipao", 0, item.Rarity.Super, 5))
            equip(player)
            self.assertIsNone(player.equipped["outfit"])

            # The player could equip the item that exists
            equip(player)
            self.assertEqual(player.equipped["outfit"].name, "qipao");
