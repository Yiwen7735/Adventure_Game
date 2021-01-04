import contextlib
import io
import unittest
from unittest.mock import create_autospec, patch

from adventure_game import action, enemy, item
from adventure_game.chest import Chest
from adventure_game.compass import Direction
from adventure_game.player import Player
from adventure_game.room import EmptyRoom, MonsterRoom
from adventure_game.trap import Trap
from adventure_game.weapon import Weapon


class FightLoopTests(unittest.TestCase):
    def test_initial_flee(self):
        """
        Tests that fleeing a fight after the initial attack works as expected.
        """
        player = Player("Tester", 100, None, None)
        first_room = EmptyRoom.generate([Direction.North])
        first_room.north = MonsterRoom.generate([Direction.South])

        player.move_to(first_room)

        def mock_input(*args):
            return "f"

        player.go(Direction.North)
        f = io.StringIO()
        with patch('builtins.input', mock_input), contextlib.redirect_stdout(f):
            action.attack(player, player.current_room.monster)

        # The player should be back in the starting room after fleeing the fight
        self.assertIs(player.current_room, first_room)
        # The previous room's description was output to stdout
        self.assertIn(str(player.current_room), f.getvalue())

    def test_fight_until_player_dead(self):
        """Tests that a fight concludes when the player dies."""
        # TODO: implement game over for this test
        pass

    def test_fight_until_enemy_dead(self):
        """Tests that a fight concludes when the enemy dies."""
        player = Player(
            "Tester",
            100,
            Weapon("sword", 0, item.Rarity.Crappy, 10, 5),
            None
        )
        monster = enemy.Enemy(
            "boss", "boss", 30, Weapon("gun", 0, item.Rarity.Crappy, 5, 5)
        )
        room = MonsterRoom("test classroom", [], monster)
        player.move_to(room)

        inputs = (i for i in ["a", "a"])

        def mock_input(*args):
            return next(inputs)

        with patch('builtins.input', mock_input):
            action.attack(player, monster)

        # Account for three attacks: one initial, two explicit in the mocked
        # inputs
        self.assertEqual(monster.is_alive(), False)

    def test_mid_fight_inventory_check(self):
        """
        Tests that a fight loop continues after a mid-fight inventory check.
        """
        player = Player("Tester", 100, None, None)
        player.move_to(MonsterRoom.generate([]))
        monster = player.current_room.monster
        initial_hp = monster.hp

        inputs = (i for i in ["a", "items", "a", "f"])

        def mock_input(*args):
            return next(inputs)

        f = io.StringIO()
        with patch('builtins.input', mock_input), contextlib.redirect_stdout(f):
            action.attack(player, monster)

        # Account for three attacks: one initial, two explicit in the mocked
        # inputs
        self.assertEqual(monster.hp, initial_hp - 3)
        # Check that the inventory was printed
        self.assertIn("Your weapons", f.getvalue())


class ChestCollectTests(unittest.TestCase):
    def test_empty_chest(self):
        player = Player("Tester", 100, None, None)
        chest = Chest()

        def mock_input(*args):
            raise RuntimeError()

        with patch('builtins.input', mock_input):
            with patch('adventure_game.chest.random.randint', lambda a, b: 0):
                action.collect(player, chest)

        self.assertEqual(chest.contents, [])

    def test_take_all_three(self):
        player = Player("Tester", 100, None, None)
        chest = Chest()

        def mock_input(*args):
            return 'take all'

        with patch('builtins.input', mock_input):
            with patch('adventure_game.chest.random.randint', lambda a, b: 3):
                action.collect(player, chest)

        self.assertEqual(chest.contents, [])
        # Check that the player's inventory now has 3 items
        self.assertEqual(
            len([i for v in player.inventory.values() for i in v]),
            3
        )

    def test_take_none(self):
        player = Player("Tester", 100, None, None)
        chest = Chest()

        def mock_input(*args):
            return 'take none'

        with patch('builtins.input', mock_input):
            with patch('adventure_game.chest.random.randint', lambda a, b: 3):
                action.collect(player, chest)

        self.assertEqual(len(chest.contents), 3)
        # Check that the player's inventory still has 0 items
        self.assertEqual(
            len([i for v in player.inventory.values() for i in v]),
            0
        )

    def test_take_first(self):
        player = Player("Tester", 100, None, None)
        chest = Chest()

        inputs = (i for i in ['take 1', 'no'])

        def mock_input(*args):
            return next(inputs)

        with patch('builtins.input', mock_input):
            with patch('adventure_game.chest.random.randint', lambda a, b: 3):
                action.collect(player, chest)

        self.assertEqual(len(chest.contents), 2)
        # Check that the player's inventory now has 1 item
        self.assertEqual(
            len([i for v in player.inventory.values() for i in v]),
            1
        )

    def test_take_first_then_second(self):
        player = Player("Tester", 100, None, None)
        chest = Chest()

        inputs = (i for i in [
            'take 1',  # Take the first item
            'yes',     # Continue taking items
            'take 2',  # Take the second item
            'no'       # Finish taking items
        ])

        def mock_input(*args):
            return next(inputs)

        with patch('builtins.input', mock_input):
            with patch('adventure_game.chest.random.randint', lambda a, b: 3):
                action.collect(player, chest)

        self.assertEqual(len(chest.contents), 1)
        # Check that the player's inventory now has 2 items
        self.assertEqual(
            len([i for v in player.inventory.values() for i in v]),
            2
        )


class SneakTests(unittest.TestCase):
    def test_failed_attempt_starts_fight(self):
        player = Player("Tester", 100)
        monster = enemy.Enemy(
            "monster", "monster", 20,
            Weapon("sword", 1, item.Rarity.Crappy, 5, 5)
        )

        attack_mock = create_autospec(action.attack)
        with patch('adventure_game.action.attack', attack_mock):
            action.attempt_sneak(player, monster)
            attack_mock.assert_called()

    def test_successful_attempt_avoids_fight(self):
        player = Player("Tester", 100)
        monster = enemy.Enemy(
            "monster", "monster", 20,
            Weapon("sword", 1, item.Rarity.Crappy, 5, 5)
        )

        attack_mock = create_autospec(action.attack)
        with patch('adventure_game.action.random.randint', lambda a, b: -1):
            with patch('adventure_game.action.attack', attack_mock):
                action.attempt_sneak(player, monster)
                attack_mock.assert_not_called()


class TriggerTrapTests(unittest.TestCase):
    def test_trigger_trap(self):
        player = Player("tester", 100, None, None)
        trap = Trap("maze", "you were stuck in a maze", 10)

        # Without any luck stats, the trap is triggered all the time
        action.trigger_trap(player, trap)
        self.assertEqual(player.hp, 90)

        # With a luck stat of 30 (> MAX_LUCK), the player is immune to trap
        weapon = Weapon("tester", 26, item.Rarity.Super, 20, 20)
        player.pick_up_item(weapon)
        player.change_item("weapon", weapon)
        action.trigger_trap(player, trap)
        self.assertEqual(player.hp, 90)

