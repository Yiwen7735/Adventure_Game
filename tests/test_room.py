import unittest

from adventure_game.compass import Direction, DIRECTIONS
from adventure_game.room import (
    EmptyRoom,
    MonsterRoom,
    NoSuchExitException,
    Room,
    TreasureRoom,
)


ALL_DIRECTIONS = ["north", "south", "east", "west"]


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
