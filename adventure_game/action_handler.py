from __future__ import annotations
from typing import Any, Callable, NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player


class ActionHandler(NamedTuple):
    description: str
    handler: Callable[[Player], Any]
