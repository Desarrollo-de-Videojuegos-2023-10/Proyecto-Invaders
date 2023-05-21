from enum import Enum


class PlayerState(Enum):
    ALIVE = 0
    DEAD = 1


class CPlayerState:
    def __init__(self, lives: int, level: int):
        self.state = PlayerState.ALIVE
        self.respawn_time = 0
        self.lives = lives
        self.levels = level
