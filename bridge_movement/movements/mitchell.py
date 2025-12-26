from collections import deque
from typing import Dict, Tuple, Any
from .generator import MovementGenerator

class MitchellMovement(MovementGenerator):
	"""
	Standalone Mitchell movements generator inheriting shared helpers.
	"""

	def __init__(self, num_pairs: int):
		super().__init__()
		if num_pairs % 2 != 0:
			raise ValueError("num_pairs must be even")
		self.num_pairs = num_pairs
		self.num_tables = num_pairs // 2
		# do not set pair_rounds here; MovementGenerator will compute them

	def initial_round(self) -> Dict[Tuple[int, str], Any]:
		pairs = [str(i + 1) for i in range(self.num_pairs)]
		ns_initial = pairs[:self.num_tables]
		ew_initial = pairs[self.num_tables: self.num_tables*2]
		round_map = {}
		for i in range(self.num_tables):
			round_map[(i + 1, 'NS')] = ns_initial[i]
			round_map[(i + 1, 'EW')] = ew_initial[i]
		return round_map

	def step(self, round_map: Dict[Tuple[int, str], Any]) -> Dict[Tuple[int, str], Any]:
		# implement Mitchell step: rotate EW pairs by -1 while NS stays same
		ew = [round_map[(i + 1, 'EW')] for i in range(self.num_tables)]
		dq = deque(ew)
		dq.rotate(-1)
		new_map = {}
		for i in range(self.num_tables):
			new_map[(i + 1, 'NS')] = round_map[(i + 1, 'NS')]
			new_map[(i + 1, 'EW')] = dq[i]
		return new_map
