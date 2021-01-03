import unittest

from adventure_game.trap import Trap, generate_trap


class TrapTests(unittest.TestCase):
    def test_trap_generation(self):
        trap = generate_trap()
        self.assertIsInstance(trap, Trap)
