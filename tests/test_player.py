import unittest

from adventure_game.compass import Direction
from adventure_game.enemy import Enemy
from adventure_game.outfit import Outfit, OutfitType
from adventure_game.player import Player
from adventure_game.room import generate_first_room
from adventure_game.weapon import Weapon, WeaponBrokenException, WeaponType


class PlayerTests(unittest.TestCase):
    def test_basic_player(self):
        player = Player(
            "Tester",
            100,
            Weapon("sword", 0, WeaponType.Crappy, 10, 10),
            Outfit("slave clothes", 0, OutfitType.Crappy, 10)
        )
        self.assertIsInstance(player, Player)

    def test_pick_up_item(self):
        player = Player(
            "Tester",
            100,
            Weapon("sword", 0, WeaponType.Crappy, 10, 10),
            Outfit("slave clothes", 0, OutfitType.Crappy, 10)
        )
        weapon = Weapon("axe", 0, WeaponType.Crappy, 5, 2)
        player.pick_up_item(weapon)
        self.assertTrue(weapon in player.inventory)

    def test_change_weapon(self):
        starting_weapon = Weapon("sword", 1, WeaponType.Crappy, 5, 5)
        player = Player(
            "Tester",
            100,
            starting_weapon,
            Outfit("pirate costume", 5, OutfitType.Solid, 5)
        )
        self.assertEqual(player.weapon, starting_weapon)
        weapon = Weapon("axe", 0, WeaponType.Solid, 10, 10)
        player.pick_up_item(weapon)
        self.assertEqual(player.weapon, starting_weapon)
        self.assertTrue(weapon in player.inventory)
        player.change_weapon(weapon)
        self.assertEqual(player.weapon, weapon)
        self.assertTrue(starting_weapon in player.inventory)

    def test_change_weapon_same_name(self):
        starting_weapon = Weapon("sword", 1, WeaponType.Crappy, 5, 5)
        player = Player(
            "Tester",
            100,
            starting_weapon,
            Outfit("pirate costume", 5, OutfitType.Solid, 5)
        )
        self.assertEqual(player.weapon, starting_weapon)
        weapon = Weapon("sword", 0, WeaponType.Solid, 10, 10)
        player.pick_up_item(weapon)
        self.assertEqual(player.weapon, starting_weapon)
        self.assertTrue(weapon in player.inventory)
        player.change_weapon(weapon)
        self.assertEqual(player.weapon, weapon)
        self.assertTrue(starting_weapon in player.inventory)

    def test_change_weapon_same_params(self):
        weapon = Weapon("sword", 1, WeaponType.Crappy, 5, 5)
        same_weapon = Weapon("sword", 1, WeaponType.Crappy, 5, 5)
        player = Player(
            "Tester",
            100,
            weapon,
            Outfit("pirate costume", 5, OutfitType.Solid, 5)
        )
        self.assertEqual(player.weapon, weapon)
        player.pick_up_item(same_weapon)
        self.assertTrue(same_weapon in player.inventory)
        player.change_weapon(same_weapon)
        self.assertEqual(player.weapon, same_weapon)
        self.assertTrue(weapon in player.inventory)

    def test_change_outfit(self):
        starting_outfit = Outfit("plain clothes", 0, OutfitType.Crappy, 1)
        player = Player(
            "Tester",
            100,
            Weapon("gun", 2, WeaponType.Super, 15, 15),
            starting_outfit
        )
        self.assertEqual(player.outfit, starting_outfit)
        outfit = Outfit("clown costume", 5, OutfitType.Solid, 10)
        player.pick_up_item(outfit)
        self.assertEqual(player.outfit, starting_outfit)
        self.assertTrue(outfit in player.inventory)
        player.change_outfit(outfit)
        self.assertEqual(player.outfit, outfit)
        self.assertTrue(starting_outfit in player.inventory)

    def test_change_outfit_same_name(self):
        starting_outfit = Outfit("plain clothes", 0, OutfitType.Crappy, 1)
        player = Player(
            "Tester",
            100,
            Weapon("gun", 2, WeaponType.Super, 15, 15),
            starting_outfit
        )
        self.assertEqual(player.outfit, starting_outfit)
        outfit = Outfit("plain_clothes", 5, OutfitType.Solid, 10)
        player.pick_up_item(outfit)
        self.assertEqual(player.outfit, starting_outfit)
        self.assertTrue(outfit in player.inventory)
        player.change_outfit(outfit)
        self.assertEqual(player.outfit, outfit)
        self.assertTrue(starting_outfit in player.inventory)

    def test_change_outfit_same_params(self):
        outfit = Outfit("armor", 1, OutfitType.Super, 50)
        same_outfit = Outfit("armor", 1, OutfitType.Super, 50)
        player = Player(
            "Tester",
            100,
            Weapon("gun", 2, WeaponType.Super, 15, 15),
            outfit
        )
        self.assertEqual(player.outfit, outfit)
        player.pick_up_item(same_outfit)
        self.assertTrue(same_outfit in player.inventory)
        player.change_outfit(same_outfit)
        self.assertEqual(player.outfit, same_outfit)
        self.assertTrue(outfit in player.inventory)

    def test_luck(self):
        weapon = Weapon("sword", 1, WeaponType.Solid, 5, 5)
        outfit = Outfit("beautiful dress", 10, OutfitType.Super, 15)
        player = Player(
            "Tester",
            100,
            weapon,
            outfit
        )
        self.assertEqual(player.get_luck(), weapon.luck_stat + outfit.luck_stat)

    def test_attack_enemy(self):
        weapon = Weapon("sword", 5, WeaponType.Solid, 5, 5)
        outfit = Outfit("qipao", 10, OutfitType.Super, 5)
        player = Player(
            "Tester",
            100,
            weapon,
            outfit
        )
        enemy = Enemy("beast", 10, Weapon("axe", 0, WeaponType.Crappy, 5, 10))
        player.attack(enemy)
        self.assertEqual(enemy.hp, 5)
        self.assertEqual(player.weapon.durability, 4)
        player.attack(enemy)
        self.assertEqual(enemy.hp, 0)
        self.assertEqual(player.weapon.durability, 3)
        player.attack(enemy)
        self.assertEqual(enemy.hp, 0)
        # Weapon durability not decremented when a hit wasn't necessary
        self.assertEqual(player.weapon.durability, 2)

    def test_attack_enemy_broken_weapon(self):
        weapon = Weapon("sword", 5, WeaponType.Solid, 5, 1)
        outfit = Outfit("qipao", 10, OutfitType.Super, 5)
        player = Player(
            "Tester",
            100,
            weapon,
            outfit
        )
        enemy = Enemy("beast", 10, Weapon("axe", 0, WeaponType.Crappy, 5, 10))
        player.attack(enemy)
        self.assertEqual(enemy.hp, 5)
        self.assertEqual(player.weapon.durability, 0)
        with self.assertRaises(WeaponBrokenException):
            player.attack(enemy)
        self.assertEqual(enemy.hp, 5)
        self.assertEqual(player.weapon.durability, 0)

    def test_attack_unarmed(self):
        player = Player("Tester", 100, None, None)
        enemy = Enemy("beast", 10, Weapon("axe", 0, WeaponType.Crappy, 5, 10))
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
        for d in room.get_exits():
            d = Direction[d]
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
