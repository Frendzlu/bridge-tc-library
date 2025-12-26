from typing import Dict, Tuple, List

from bridge_movement import Position, Table, Pair, BoardGroup

type mov_strat = list[
	Tuple[
		list[
			Tuple[
				Tuple[Table, Position],
				Tuple[Table, Position]
			]
		],
		list[int]
	]
]

class Movement:
	tables: list['Table']
	boards: list['BoardGroup']
	pairs: list['Pair']

	def __init__(self, tables: list[Table], boards: list[BoardGroup], pairs: list[Pair], movement_strategies: mov_strat ):
		self.tables = tables
		self.boards = boards
		self.pairs = pairs

	def get_sitting_for_round(self, round_number: int) -> Dict[Table, Dict[Position, Pair]]:
		"""
		{(table_name, position): Pair}
		"""
		pass

	def get_boards_for_round(self, current_boards: dict) -> dict:
		"""
		{table_name: BoardGroup}
		"""
		pass
