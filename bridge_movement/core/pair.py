from dataclasses import dataclass
from typing import Tuple
from .player import Player

@dataclass(frozen=True)
class Pair:
	id: str
	players: Tuple[Player, Player]
