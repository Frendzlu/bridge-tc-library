from typing import Dict, Type

from .table import Table
from bridge_movement import BoardGroup
from bridge_movement import RotationalMovement


class Sector:
    def __init__(self, name, min_boards=0, max_boards=0):
        self.movement = None
        self.name = name
        self.tables = []
        self.board_groups: Dict[int, 'BoardGroup'] = {}
        self.max_boards = 0
        self.min_boards = 0

    def set_movement(self, movement_cls: Type[RotationalMovement]):
        self.movement = movement_cls(self.tables, self.min_boards, self.max_boards)

    def add_tables(self, table_num):
        for i in range(table_num):
            table = Table(table_id=i + 1, sector=self)
            self.tables.append(table)

    def advance_round(self):
        for table in self.tables:
            print(table)

