import unittest

from adventure_game.constants import MAX_LUCK
from adventure_game.compass import Direction
from adventure_game.enemy import Enemy
from adventure_game.exceptions import InventoryFullException
from adventure_game.item import Rarity
from adventure_game.outfit import Outfit
from adventure_game.player import Player
from adventure_game.room import (
    generate_first_room, EmptyRoom, NoSuchExitException
)
from adventure_game.weapon import Weapon, generate_weapon, WeaponBrokenException


class PlayerTests(unittest.TestCase):
    def test_basic_player(self):
        player = Player(
            "Tester",
            100,
            Weapon("sword", 0, Rarity.Crappy, 10, 10),
            Outfit("slave clothes", 0, Rarity.Crappy, 10)
        )
        self.assertIsInstance(player, Player)

    def test_pick_up_item(self):
        player = Player(
            "Tester",
            100,
            Weapon("sword", 0, Rarity.Crappy, 10, 10),
            Outfit("slave clothes", 0, Rarity.Crappy, 10)
        )
        weapon = Weapon("axe", 0, Rarity.Crappy, 5, 2)
        outfit = Outfit("qipao", 10, Rarity.Super, 10)
        player.pick_up_item(weapon)
        player.pick_up_item(outfit)
        self.assertTrue(weapon in player.weapons)
        self.assertTrue(outfit in player.outfits)

    def test_pick_up_item_with_full_pocket(self):
        player = Player("Tester", 100, None, None)
        for i in range(10):
            player.pick_up_item(generate_weapon())

        # After reaching 10, the player is not allowed to pick another weapon
        weapon = generate_weapon()
        with self.assertRaises(InventoryFullException):
            player.pick_up_item(weapon)
        self.assertFalse(weapon in player.weapons)

    def test_change_weapon(self):
        starting_weapon = Weapon("sword", 1, Rarity.Crappy, 5, 5)
        player = Player(
            "Tester",
            100,
            starting_weapon,
            Outfit("pirate costume", 5, Rarity.Common, 5)
        )
        self.assertEqual(player.cur_weapon, starting_weapon)
        weapon = Weapon("axe", 0, Rarity.Common, 10, 10)
        player.pick_up_item(weapon)
        self.assertEqual(player.cur_weapon, starting_weapon)
        self.assertTrue(weapon in player.weapons)
        player.change_item("weapon", weapon)
        self.assertEqual(player.cur_weapon, weapon)
        self.assertTrue(starting_weapon in player.weapons)

    def test_change_weapon_same_name(self):
        starting_weapon = Weapon("sword", 1, Rarity.Crappy, 5, 5)
        player = Player(
            "Tester",
            100,
            starting_weapon,
            Outfit("pirate costume", 5, Rarity.Common, 5)
        )
        self.assertEqual(player.cur_weapon, starting_weapon)
        weapon = Weapon("sword", 0, Rarity.Common, 10, 10)
        player.pick_up_item(weapon)
        self.assertEqual(player.cur_weapon, starting_weapon)
        self.assertTrue(weapon in player.weapons)
        player.change_item("weapon", weapon)
        self.assertEqual(player.cur_weapon, weapon)
        self.assertTrue(starting_weapon in player.weapons)

    def test_change_weapon_same_params(self):
        weapon = Weapon("sword", 1, Rarity.Crappy, 5, 5)
        same_weapon = Weapon("sword", 1, Rarity.Crappy, 5, 5)
        player = Player(
            "Tester",
            100,
            weapon,
            Outfit("pirate costume", 5, Rarity.Common, 5)
        )
        self.assertEqual(player.cur_weapon, weapon)
        player.pick_up_item(same_weapon)
        self.assertTrue(same_weapon in player.weapons)
        player.change_item("weapon", same_weapon)
        self.assertEqual(player.cur_weapon, same_weapon)
        self.assertTrue(weapon in player.weapons)

    def test_change_outfit(self):
        starting_outfit = Outfit("plain clothes", 0, Rarity.Crappy, 1)
        player = Player(
            "Tester",
            100,
            Weapon("gun", 2, Rarity.Super, 15, 15),
            starting_outfit
        )
        self.assertEqual(player.cur_outfit, starting_outfit)
        outfit = Outfit("clown costume", 5, Rarity.Common, 10)
        player.pick_up_item(outfit)
        self.assertEqual(player.cur_outfit, starting_outfit)
        self.assertTrue(outfit in player.outfits)
        player.change_item("outfit", outfit)
        self.assertEqual(player.cur_outfit, outfit)
        self.assertTrue(starting_outfit in player.outfits)

    def test_change_outfit_same_name(self):
        starting_outfit = Outfit("plain clothes", 0, Rarity.Crappy, 1)
        player = Player(
            "Tester",
            100,
            Weapon("gun", 2, Rarity.Super, 15, 15),
            starting_outfit
        )
        self.assertEqual(player.cur_outfit, starting_outfit)
        outfit = Outfit("plain_clothes", 5, Rarity.Common, 10)
        player.pick_up_item(outfit)
        self.assertEqual(player.cur_outfit, starting_outfit)
        self.assertTrue(outfit in player.outfits)
        player.change_item("outfit", outfit)
        self.assertEqual(player.cur_outfit, outfit)
        self.assertTrue(starting_outfit in player.outfits)

    def test_change_outfit_same_params(self):
        outfit = Outfit("armor", 1, Rarity.Super, 50)
        same_outfit = Outfit("armor", 1, Rarity.Super, 50)
        player = Player(
            "Tester",
            100,
            Weapon("gun", 2, Rarity.Super, 15, 15),
            outfit
        )
        self.assertEqual(player.cur_outfit, outfit)
        player.pick_up_item(same_outfit)
        self.assertTrue(same_outfit in player.outfits)
        player.change_item("outfit", same_outfit)
        self.assertEqual(player.cur_outfit, same_outfit)
        self.assertTrue(outfit in player.outfits)

    def test_luck(self):
        weapon = Weapon("sword", 1, Rarity.Common, 5, 5)
        outfit = Outfit("beautiful dress", 10, Rarity.Super, 15)
        player = Player("Tester", 100, weapon, outfit)
        self.assertEqual(player.get_luck(), weapon.luck_stat + outfit.luck_stat)

    def test_luck_no_equipped_items(self):
        player = Player("Tester", 100)
        self.assertEqual(player.get_luck(), 0)

    def test_luck_greater_than_max(self):
        weapon = Weapon("sword", MAX_LUCK + 1, Rarity.Common, 5, 5)
        outfit = Outfit("beautiful dress", MAX_LUCK + 10, Rarity.Super, 15)
        player = Player("Tester", 100, weapon, outfit)
        self.assertEqual(player.get_luck(), MAX_LUCK)

    def test_attack_enemy(self):
        weapon = Weapon("sword", 5, Rarity.Common, 5, 5)
        outfit = Outfit("qipao", 10, Rarity.Super, 5)
        player = Player("Tester", 100, weapon, outfit)
        enemy = Enemy(
            "beast", "beast", 10, Weapon("axe", 0, Rarity.Crappy, 5, 10)
        )
        player.attack(enemy)
        self.assertEqual(enemy.hp, 5)
        self.assertEqual(player.cur_weapon.durability, 4)
        player.attack(enemy)
        self.assertEqual(enemy.hp, 0)
        self.assertEqual(player.cur_weapon.durability, 3)
        player.attack(enemy)
        self.assertEqual(enemy.hp, 0)
        # Weapon durability not decremented when a hit wasn't necessary
        self.assertEqual(player.cur_weapon.durability, 2)

    def test_attack_enemy_broken_weapon(self):
        weapon = Weapon("sword", 5, Rarity.Common, 5, 1)
        outfit = Outfit("qipao", 10, Rarity.Super, 5)
        player = Player("Tester", 100, weapon, outfit)
        enemy = Enemy(
            "beast", "best", 10, Weapon("axe", 0, Rarity.Crappy, 5, 10)
        )
        player.attack(enemy)
        self.assertEqual(enemy.hp, 5)
        self.assertEqual(player.cur_weapon.durability, 0)
        with self.assertRaises(WeaponBrokenException):
            player.attack(enemy)
        self.assertEqual(enemy.hp, 5)
        self.assertEqual(player.cur_weapon.durability, 0)

    def test_attack_unarmed(self):
        player = Player("Tester", 100, None, None)
        enemy = Enemy(
            "beast", "beast", 10, Weapon("axe", 0, Rarity.Crappy, 5, 10)
        )
        player.attack(enemy)
        self.assertEqual(enemy.hp, 9)


class PlayerMovementTests(unittest.TestCase):
    def test_initial_placement(self):
        room = generate_first_room()
        player = Player("Tester", 100, None, None)
        player.move_to(room)
        self.assertEqual(player.current_room, room)

    def test_initial_placement_retreat(self):
        room = generate_first_room()
        player = Player("Tester", 100, None, None)
        player.move_to(room)
        self.assertEqual(player.current_room, room)
        player.retreat()
        self.assertEqual(player.current_room, None)

    def test_go_valid_directions(self):
        room = generate_first_room()
        player = Player("Tester", 100, None, None)
        player.move_to(room)
        for d in room.exits:
            if d is Direction.North:
                new_room = player.current_room.north
            elif d is Direction.South:
                new_room = player.current_room.south
            elif d is Direction.East:
                new_room = player.current_room.east
            else:
                new_room = player.current_room.west
            player.go(d)
            self.assertEqual(player.current_room, new_room)
            player.retreat()
            self.assertEqual(player.current_room, room)

    def test_go_invalid_direction(self):
        room = EmptyRoom("", [Direction.North])
        player = Player("Tester", 100, None, None)
        player.move_to(room)
        with self.assertRaises(NoSuchExitException):
            player.go(Direction.South)
