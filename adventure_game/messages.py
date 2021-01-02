from typing import Any, List

from .room import Room


def get_a_or_an(s: str) -> str:
    """
    Determines whether the singular counter for a string should be 'a' or 'an'.

    Args:
        s: The string to analyze.

    Returns:
        'an' if s starts with a vowel sound, 'a' otherwise.

    """
    if any(s.startswith(c) for c in ['a', 'e', 'i', 'o', 'u', 'honor']):
        return 'an'
    return 'a'


def list_to_comma_string(options: List[Any]) -> str:
    """
    Convert a list of items to a comma-separated string, including and
    separation for the last element.

    Args:
        options: A list of any type that implements __str__.

    Returns:
        Combined string representation.

    """
    if not options:
        return ''
    if len(options) == 1:
        return str(options[0])
    return ', '.join(str(o) for o in options[:-1]) + f' and {options[-1]}'


def print_enter(room: Room):
    """Prints a message indicating the entered room."""
    print(f"You enter {room}.")
