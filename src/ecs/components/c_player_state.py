from enum import Enum

class PlayerState(Enum):
    IDLE = 0
    DEAD = 1

class CPlayerState:
    def __init__(self, lives:int):
        self.state = PlayerState.IDLE
        self.respawn_time = 0
        self.lives = lives