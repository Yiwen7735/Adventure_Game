import unittest
from unittest.mock import patch

from adventure_game import item, room
from adventure_game.compass import Direction
from adventure_game.outfit import Outfit
from adventure_game.player import Player
from adventure_game.utils import drop, equip, parse_movement_instr, throw
from adventure_game.weapon import Weapon


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
            self.assertEqual(player.equipped["outfit"].name, "qipao")


class ThrowTests(unittest.TestCase):
    def test_throw_weapon(self):
        weapon = Weapon("gun", 5, item.Rarity.Super, 10, 10)
        player = Player("Tester", 100, weapon, None)
        first_room = room.EmptyRoom.generate([])
        player.move_to(first_room)
        throw(player)
        self.assertIsNone(player.equipped["weapon"])
        self.assertFalse(weapon in player.inventory['weapon'])
        self.assertIn(weapon, first_room.items)


class DropTests(unittest.TestCase):
    def test_drop_items(self):
        player = Player("Tester", 100, None, None)
        weapon = Weapon("sword", 5, item.Rarity.Common, 10, 10)
        outfit = Outfit("vest", 6, item.Rarity.Super, 20)
        player.pick_up_item(weapon)
        player.pick_up_item(outfit)

        first_room = room.EmptyRoom.generate([])
        player.move_to(first_room)

        inputs = (i for i in ["w1", "o2", "o1"])

        def mock_input(*args):
            return next(inputs)

        with patch("builtins.input", mock_input):
            drop(player)
            self.assertFalse(weapon in player.inventory["weapon"])
            self.assertIn(weapon, first_room.items)
            drop(player)
            self.assertTrue(outfit in player.inventory["outfit"])
            self.assertNotIn(outfit, first_room.items)
            drop(player)
            self.assertFalse(outfit in player.inventory["outfit"])
            self.assertIn(outfit, first_room.items)

            # The equipped items are still none
            self.assertIsNone(player.equipped["weapon"])
            self.assertIsNone(player.equipped["outfit"])
