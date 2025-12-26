from bridge_movement.core import Pair, BoardGroup, Player
from .table import Table
from .tournament import Tournament
from .sector import Sector
from bridge_movement.movement.rotational import RotationalMovement
from typing import Type


class AutoTournament(Tournament):
	"""
	Automatically generates sectors, tables, assigns non-overlapping pairs,
	and allocates board numbers from a single tournament pool.
	"""

	def __init__(self, total_pairs, total_boards):
		super().__init__(total_boards=total_boards)
		self.total_pairs = total_pairs
		self.generated_pairs = self._generate_pairs(total_pairs)
		self.used_pairs = set()
		self._next_board = 1

	def _generate_pairs(self, n):
		return [Pair(str(i + 1), (Player(), Player())) for i in range(n)]

	def add_sector_auto(self, sector_name, num_tables, movement_cls: Type[RotationalMovement],
	                    boards_per_round: int = 1):
		"""
		Adds a sector using the given movement class (e.g., MitchellMovement).
		Non-overlapping pairs are automatically assigned.

		:param sector_name: name of the sector
		:param num_tables: number of tables in the sector
		:param movement_cls: RotationalMovement subclass to use
		:param boards_per_round: how many board numbers each table plays per round
		:return: Sector object
		"""

		available_pairs = [p for p in self.generated_pairs if p not in self.used_pairs]
		if len(available_pairs) < num_tables * 2:
			raise ValueError(f"Not enough remaining pairs for {num_tables} tables in sector {sector_name}.")

		ns_pairs = available_pairs[:num_tables]
		ew_pairs = available_pairs[num_tables:num_tables * 2]

		for p in ns_pairs + ew_pairs:
			self.used_pairs.add(p)

		sector = Sector(sector_name)

		tables = [Table(i + 1, sector) for i in range(num_tables)]

		# Create movement
		movement = movement_cls(tables=tables, ns_pairs=ns_pairs, ew_pairs=ew_pairs)

		# Determine rounds / board allocation
		if boards_per_round <= 0:
			raise ValueError("boards_per_round must be >= 1")

		rounds = self.total_boards // boards_per_round
		board_start = self._next_board

		if board_start + rounds * boards_per_round - 1 > self.total_boards:
			raise ValueError("Requested board allocation exceeds tournament total boards")

		groups = []
		start = board_start
		for _ in range(rounds):
			end = start + boards_per_round - 1
			group = tuple(range(start, end + 1))
			groups.append(group)
			start = end + 1

		board_rounds = []
		for r in range(rounds):
			mapping = {}
			for i, t in enumerate(tables):
				grp = groups[(i + r) % rounds]
				mapping[t] = BoardGroup(grp)
			board_rounds.append(mapping)

		movement.board_rounds = board_rounds

		sector = Sector(sector_name, tables, movement, boards_per_round=boards_per_round)
		sector.set_initial_state(movement.get_first_round(), board_rounds[0])
		self.add_sector(sector)
		return sector
