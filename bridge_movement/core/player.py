from dataclasses import dataclass

@dataclass(frozen=True)
class Player:
	name: str = ""
	db_id: str = ""
