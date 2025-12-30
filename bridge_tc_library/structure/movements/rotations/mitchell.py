from collections import deque
from typing import List, Dict, Tuple, Any

from bridge_tc_library.structure import MovementStrategy
from bridge_tc_library.structure.movements.abstract_rotation import AbstractRotation


class MitchellMovement(AbstractRotation):
	"""
	Standalone Mitchell movements generator inheriting shared helpers.
	Mitchell operates always on just one boardgroup_set, and it always uses boards_amount = tables_amount * n were n = {1, 2, 3, ...}
	"""

	def __init__(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int, min_boards_per_boardgroup: int = 2):
		super().__init__()
		self.num_pairs = num_pairs
		self.min_boards_amount = min_boards_amount
		self.max_boards_amount = max_boards_amount
		self.min_boards_per_boardgroup = min_boards_per_boardgroup
		self.bye = self.check_if_bye_needed(self.num_pairs)

	def check_if_can_handle(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int, min_boards_per_boardgroup: int = 2) -> bool:
		num_tables = num_pairs // 2
		if num_tables < 3 or num_tables % 2 == 0:
			return False
		elif max_boards_amount // min_boards_per_boardgroup < num_tables:
			return False
		else:
			n=0
			while num_tables*(min_boards_amount+n)<=max_boards_amount:
				if num_tables*(min_boards_amount+n)> min_boards_amount:
					return True
				n +=1
			return False

	def generate_strategy_for_rotation(self, num_pairs: int, rounds: int, boardgroup_sets: int) -> MovementStrategy:
		pass

	def generate_possibile_rotations_draft(self, num_pairs: int, max_boards_amount: int) -> \
	List[Tuple[int, int, int]]:
		list_of_rotations: List[Tuple[int, int, int]] = []
		num_tables = num_pairs // 2
		boards_per_boardgroup = self.min_boards_per_boardgroup
		while boards_per_boardgroup * num_tables <= max_boards_amount:
			total_boards = boards_per_boardgroup * num_tables
			list_of_rotations.append((num_tables, total_boards, 1))
			boards_per_boardgroup += 1
		return list_of_rotations


	
