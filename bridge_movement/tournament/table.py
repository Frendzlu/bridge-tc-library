from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .sector import Sector
    from bridge_movement import Pair, Position, BoardGroup

class Table:
    def __init__(self, table_id: int, sector: 'Sector') -> None:
        self.table_id: int = table_id
        self.sector: 'Sector' = sector
        self.current_round: Optional[int] = None
        self.current_pairs: Optional[dict['Position', 'Pair']] = None
        self.current_board: Optional[int] = None
        self.current_board_set: Optional['BoardGroup'] = None

    def next_deal(self):
        if self.current_round is None:
            raise ValueError("Table has not started any round yet.")

    def start(self, ns_pair: 'Pair', ew_pair: 'Pair', board_set: 'BoardGroup'):
        self.current_round = 1
        self.current_pairs = {
            Position.NS: ns_pair,
            Position.EW: ew_pair
        }
        self.current_board = board_set.boards[0]
        self.current_board_set = board_set

    def next_deal(self):
        if self.current_round is None:
            raise ValueError("Table has not started any round yet.")

        if self.current_board_set.boards.index(self.current_board) + 1 > len(self.current_board_set.boards):
            next_index = self.current_board_set.boards.index(self.current_board) + 1
            self.current_board = self.current_board_set.boards[next_index]
