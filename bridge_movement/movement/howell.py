from .rotational import RotationalMovement
from collections import deque

class HowellMovement(RotationalMovement):
	"""
	Howell movement:
	- Boards move down one table each round (Mitchell-style).
	- Highest-numbered pair is stationary at Table1 NS.
	- Pair '1' starts at Table1 EW. The remaining pairs follow the Howell wheel.
	"""

	def __init__(self, tables, ns_pairs=None, ew_pairs=None, initial_boards=None):
		super().__init__(tables, ns_pairs or [], ew_pairs or [], initial_boards)

		# Combine pairs: keep order as provided (ns_pairs then ew_pairs) if possible
		all_pairs = [p for p in list(self.ns_pairs) + list(self.ew_pairs) if p is not None]
		num_tables = len(self.tables)
		expected_pairs = 2 * num_tables

		# Pad if insufficient
		# If not enough pairs provided, pad with None to expected size
		if len(all_pairs) < expected_pairs:
			# We'll fill with None placeholders at the end (phantom sit-out possible)
			all_pairs = all_pairs + [None] * (expected_pairs - len(all_pairs))

		# Determine stationary (highest-numbered by id) and others in numeric order
		# Filter out None, sort numerically by pair.id
		numeric_pairs = [p for p in all_pairs if p is not None]
		numeric_pairs_sorted = sorted(numeric_pairs, key=lambda p: int(getattr(p, 'id')))
		if numeric_pairs_sorted:
			stationary = numeric_pairs_sorted[-1]
			others_sorted = [p for p in numeric_pairs_sorted if p != stationary]
		else:
			stationary = None
			others_sorted = []

		# Build the wheel order so that pair 1 follows the second-highest pair: [2,3,...,S,1]
		if len(others_sorted) > 0:
			if len(others_sorted) == 1:
				wheel_base = [others_sorted[0]]
			else:
				# rotate left by 1: [1,2,3,...,S] -> [2,3,...,S,1]
				wheel_base = others_sorted[1:] + [others_sorted[0]]
		else:
			wheel_base = []

		dq = deque(wheel_base)
		# Ensure pair '1' is positioned to be at Table1 EW (dq index num_tables-1)
		if wheel_base:
			try:
				index_pair1 = next(i for i, p in enumerate(wheel_base) if getattr(p, 'id', None) == '1')
			except StopIteration:
				index_pair1 = 0
			rotate_amount = (num_tables - 1 - index_pair1) % len(wheel_base)
			dq.rotate(rotate_amount)

		rounds = []
		total_rounds = 2 * num_tables - 1
		for _ in range(total_rounds):
			# build flat positions: stationary at index 0, then deque elements
			positions = [stationary] + list(dq)
			round_map = {}
			for i, table in enumerate(self.tables):
				ns_pair = positions[i]
				ew_pair = positions[i + num_tables]
				round_map[(table, "NS")] = ns_pair
				round_map[(table, "EW")] = ew_pair
			rounds.append(round_map)
			dq.rotate(-1)

		self.pair_rounds = rounds

	def next_pairs_round(self, current_round: dict) -> dict:
		try:
			i = self.pair_rounds.index(current_round)
		except ValueError:
			raise StopIteration("Current round not found in Howell pair rounds")

		if i + 1 >= len(self.pair_rounds):
			raise StopIteration
		return self.pair_rounds[i + 1]

	def next_boards_round(self, current_boards):
		"""
		Boards move up one table each round (wrap-around), like Mitchell movement.
		"""
		# If explicit board_rounds sequence is configured, use it (one mapping per round)
		if hasattr(self, 'board_rounds') and len(self.board_rounds) > 1:
			return super().next_boards_round(current_boards)

		next_boards = {}
		for i, table in enumerate(self.tables):
			prev_table = self.tables[i - 1]  # wrap-around
			next_boards[table] = current_boards[prev_table]
		return next_boards
