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
        equip(player, "w1")
        # The player should not be able to equip non-existent items
        self.assertIsNone(player.cur_weapon)
        player.pick_up_item(Outfit("qipao", 0, item.Rarity.Super, 5))
        equip(player, "o2")
        self.assertIsNone(player.cur_outfit)

        # The player could equip the item that exists
        equip(player, "o1")
        self.assertEqual(player.cur_outfit.name, "qipao")


class ThrowTests(unittest.TestCase):
    def test_throw_weapon(self):
        weapon = Weapon("gun", 5, item.Rarity.Super, 10, 10)
        player = Player("Tester", 100, weapon, None)
        first_room = room.EmptyRoom.generate([])
        player.move_to(first_room)
        throw(player)
        self.assertIsNone(player.cur_weapon)
        self.assertFalse(weapon in player.weapons)
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

        drop(player, "w1")
        self.assertFalse(weapon in player.weapons)
        self.assertIn(weapon, first_room.items)
        drop(player, "o2")
        self.assertTrue(outfit in player.outfits)
        self.assertNotIn(outfit, first_room.items)
        drop(player, "o1")
        self.assertFalse(outfit in player.outfits)
        self.assertIn(outfit, first_room.items)

        # The equipped items are still none
        self.assertIsNone(player.cur_weapon)
        self.assertIsNone(player.cur_outfit)
