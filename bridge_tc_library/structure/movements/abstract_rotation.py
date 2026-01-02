from typing import List, Optional, Any, Tuple, Dict
from abc import ABC, abstractmethod
from .strategy import MovementStrategy
from bridge_tc_library.structure.core import Position
from bridge_tc_library.structure.tournament import Table


class AbstractRotation(ABC):
	num_tables: int
	"""
	Abstract base class for rotation calculators.
	"""

	def __init__(self):
		self._pair_rounds_cache: Optional[List[Dict[Tuple[int, str], Any]]] = None

	@abstractmethod
	def check_if_can_handle(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int, min_boards_per_boardgroup: int = 2) -> bool:
		"""
		Checks if the current rotation can handle the given number of pairs and boardgroups.
		"""

	@abstractmethod
	def generate_possibile_rotations_draft(self, num_pairs: int, max_boards_amount: int) -> List[Tuple[int, int, int]]:
		"""
		Generates possible rotation drafts.
		This will generate a list of possible rotations in a draft format.
		List of tuples: (Amount of rounds: int, Amount of boards: int, amount of boardgroup_sets: int)
		"""

	@abstractmethod
	def generate_strategy_for_rotation(self, num_pairs: int, num_rounds: int, num_boardgroup_sets: int, Tables: Tuple[Table], optional_arg: Optional[Any] = None) -> MovementStrategy:
		"""
		Generates movement strategy for the given rotation parameters.
		"""

	def check_if_bye_needed(self, num_pairs: int) -> bool:
		"""
		Indicates if bye is needed in the rotation.
		If so, one pair will be added to the total number of pairs, so it is even.
		"""
		if num_pairs % 2 == 1:
			self.num_pairs += 1
			return True
		else:
			return False

	
