import unittest

from adventure_game.outfit import Outfit, generate_outfit


class OutfitGenerationTests(unittest.TestCase):
    def test_basic(self):
        outfit = generate_outfit()
        self.assertIsInstance(outfit, Outfit)
