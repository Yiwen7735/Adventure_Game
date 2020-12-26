import enum
import random
from typing import List


class Direction(enum.Enum):
    North = enum.auto()
    South = enum.auto()
    East = enum.auto()
    West = enum.auto()


DIRECTIONS = [Direction.North, Direction.South, Direction.East, Direction.West]


def get_opposite_dir(d: Direction) -> Direction:
    """
    Determine the opposite compass direction of 'd'.

    Args:
        d: The compass direction to invert.

    Returns:
        The direction opposite to the input, e.g. North, when given South.

    """
    if d == Direction.North:
        return Direction.South
    if d == Direction.South:
        return Direction.North
    if d == Direction.East:
        return Direction.West
    return Direction.East


def get_random_directions() -> List[Direction]:
    n = random.randint(1, 4)
    return random.sample(DIRECTIONS, n)
