from enum import Enum

class PlayState(Enum):
    START = 0
    PLAYING = 1
    WIN = 2
    LOSE = 3



class CPlayState:
    def __init__(self) -> None:
        self.state = PlayState.START
        self.time = 0