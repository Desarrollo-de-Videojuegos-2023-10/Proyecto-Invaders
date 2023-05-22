from enum import Enum

class MovementDirection(Enum):
    LEFT = 0
    RIGHT = 1

class CEnemyState:
    def __init__(self) -> None:
        self.movement_direction = MovementDirection.RIGHT