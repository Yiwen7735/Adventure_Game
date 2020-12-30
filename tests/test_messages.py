import unittest

from adventure_game.messages import get_a_or_an


class GrammarTests(unittest.TestCase):
    def test_a_or_an_vowel(self):
        self.assertEqual(get_a_or_an('enemy'), 'an')

    def test_a_or_an_consonant(self):
        self.assertEqual(get_a_or_an('monster'), 'a')

    def test_a_or_an_silent_h(self):
        self.assertEqual(get_a_or_an('honorable swordsman'), 'an')
