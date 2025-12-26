from collections import deque
from bridge_movement.core.movement_strategy import MovementStrategy
from bridge_movement.core.board_group import BoardGroup

class MitchellMovement(MovementStrategy):
	"""
	Mitchell rotation:
	- NS pairs stationary
	- EW pairs rotate
	- Boards rotate down one table each round
	"""