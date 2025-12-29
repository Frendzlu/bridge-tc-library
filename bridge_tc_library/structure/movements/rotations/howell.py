from collections import deque
from typing import List, Dict, Tuple, Any

from bridge_tc_library.structure import MovementStrategy
from bridge_tc_library.structure.movements.abstract_rotation import AbstractRotation


class HowellMovement(AbstractRotation):
	"""
	Standalone Howell movements generator inheriting shared helpers.
	"""
	def __init__(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int):
		super().__init__()
		self.num_pairs = num_pairs
		self.min_boards_amount = min_boards_amount
		self.max_boards_amount = max_boards_amount
		self.bye = self.check_if_bye_needed(self.num_pairs)

	def check_if_can_handle(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int) -> bool:
		pass

	def generate_possibile_rotations_draft(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int) -> \
	List[Tuple[int, int, int]]:
		pass

	def generate_strategy_for_rotation(self, num_pairs: int, rounds: int, boardgroup_sets: int) -> MovementStrategy:
		pass

