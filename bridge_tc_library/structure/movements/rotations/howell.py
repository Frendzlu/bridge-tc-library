from collections import deque
from typing import List, Dict, Tuple, Any

from bridge_tc_library.structure import MovementStrategy
from bridge_tc_library.structure.movements.abstract_rotation import AbstractRotation


class HowellMovement(AbstractRotation):
	"""
	Standalone Howell movements generator inheriting shared helpers.
	How does howell work:
	basic: all vs all, num_round = num_pairs - 1
	reduced: for bigger, (num_pairs*3/4 -1) <= num_rounds <= (num_pairs - 1)
	"""
	def __init__(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int, min_boards_per_boardgroup: int = 2):
		super().__init__()
		self.num_pairs = num_pairs
		self.min_boards_amount = min_boards_amount
		self.max_boards_amount = max_boards_amount
		self.bye = self.check_if_bye_needed(self.num_pairs)

	def check_if_can_handle(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int, min_boards_per_boardgroup: int = 2) -> bool:
		return True
	def generate_possibile_rotations_draft(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int) -> \
	List[Tuple[int, int, int]]:
		"""
		Generates possible rotation drafts.
		This will generate a list of possible rotations in a draft format.
		List of tuples: (Amount of rounds: int, Amount of boards: int, amount of boardgroup_sets: int)
		"""
		pass

	def generate_strategy_for_rotation(self, num_pairs: int, rounds: int, boardgroup_sets: int) -> MovementStrategy:

		pass

