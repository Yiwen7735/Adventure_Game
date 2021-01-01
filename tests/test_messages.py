import unittest

from adventure_game.compass import Direction
from adventure_game.messages import get_a_or_an, list_to_comma_string


class GrammarTests(unittest.TestCase):
    def test_a_or_an_vowel(self):
        self.assertEqual(get_a_or_an('enemy'), 'an')

    def test_a_or_an_consonant(self):
        self.assertEqual(get_a_or_an('monster'), 'a')

    def test_a_or_an_silent_h(self):
        self.assertEqual(get_a_or_an('honorable swordsman'), 'an')


class ListToStringTests(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(list_to_comma_string([]), '')

    def test_one_element_list(self):
        self.assertEqual(list_to_comma_string(['first']), 'first')

    def test_two_element_list(self):
        self.assertEqual(
            list_to_comma_string(['first', 'second']),
            'first and second'
        )

    def test_three_element_list(self):
        self.assertEqual(
            list_to_comma_string(['first', 'second', 'third']),
            'first, second and third'
        )

    def test_five_element_list(self):
        self.assertEqual(
            list_to_comma_string(
                ['first', 'second', 'third', 'fourth', 'fifth']
            ),
            'first, second, third, fourth and fifth'
        )

    def test_direction_list(self):
        self.assertEqual(
            list_to_comma_string(
                [Direction.North, Direction.South, Direction.East,
                 Direction.West]
            ),
            'North, South, East and West'
        )
