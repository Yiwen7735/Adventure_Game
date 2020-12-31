import unittest
from unittest.mock import patch

from adventure_game.compass import Direction, DIRECTIONS
from adventure_game.room import (
    EmptyRoom,
    MonsterRoom,
    NoSuchExitException,
    Room,
    TreasureRoom,
    generate_first_room,
)
from adventure_game.weapon import Weapon


ALL_DIRECTIONS = ["north", "south", "east", "west"]


class GenerateFirstRoomTests(unittest.TestCase):
    def test_is_empty_room(self):
        room = generate_first_room()
        self.assertIsInstance(room, EmptyRoom)


class GenericRoomTests(unittest.TestCase):
    def test_basic_generate(self):
        for cls in [EmptyRoom, MonsterRoom, TreasureRoom]:
            with self.subTest():
                room = cls.generate([])
                self.assertIsInstance(room, cls)
                for d in ALL_DIRECTIONS:
                    with self.assertRaises(NoSuchExitException):
                        getattr(room, d)

    def test_generate_one_exit(self):
        for cls in [EmptyRoom, MonsterRoom, TreasureRoom]:
            with self.subTest():
                room = cls.generate([Direction.North])
                next_room = room.north
                self.assertIsInstance(next_room, Room)
                self.assertEqual(next_room, room.north)
                self.assertEqual(room, next_room.south)

    def test_generate_all_exits(self):
        for cls in [EmptyRoom, MonsterRoom, TreasureRoom]:
            with self.subTest():
                room = cls.generate(DIRECTIONS)
                next_room = room.east
                self.assertIsInstance(next_room, Room)
                self.assertEqual(next_room, room.east)
                self.assertEqual(room, next_room.west)
                self.assertEqual(
                    len([room.north, room.south, room.east, room.west, self]),
                    5
                )


class EmptyRoomTests(unittest.TestCase):
    def test_random_weapon(self):
        # Mock the random.randint function to guarantee that a weapon should
        # be added to the room
        with patch('adventure_game.room.random.randint', lambda a, b: 1):
            room = EmptyRoom.generate([])
        self.assertIsInstance(room.weapon, Weapon)

    def test_no_random_weapon(self):
        # Mock the random.randint function to guarantee that a weapon should
        # not be added to the room
        with patch('adventure_game.room.random.randint', lambda a, b: 0):
            room = EmptyRoom.generate([])
        self.assertIsNone(room.weapon)
