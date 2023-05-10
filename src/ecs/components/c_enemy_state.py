from enum import Enum

class EnemyState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2

class MovementDirection(Enum):
    LEFT = 0
    RIGHT = 1

class CEnemyState:
    def __init__(self) -> None:
        self.state = EnemyState.IDLE
        self.movement_direction = MovementDirection.RIGHT