import unittest

from adventure_game.room import (
    EmptyRoom,
    MonsterRoom,
    TreasureRoom,
    generate_empty_room,
    generate_monster_room,
    generate_treasure_room,
)


class EmptyRoomTests(unittest.TestCase):
    def test_generate(self):
        room = generate_empty_room()
        self.assertIsInstance(room, EmptyRoom)


class MonsterRoomTests(unittest.TestCase):
    def test_generate(self):
        room = generate_monster_room()
        self.assertIsInstance(room, MonsterRoom)


class TreasureRoomTests(unittest.TestCase):
    def test_generate(self):
        room = generate_treasure_room()
        self.assertIsInstance(room, TreasureRoom)
