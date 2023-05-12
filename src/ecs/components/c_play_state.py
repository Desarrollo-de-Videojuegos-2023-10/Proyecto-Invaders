from enum import Enum

class PlayState(Enum):
    START = 0
    PLAYING = 1
    WIN = 2
    GAME_OVER = 3
    END = 4



class CPlayState:
    def __init__(self) -> None:
        self.state = PlayState.START
        self.time = 0