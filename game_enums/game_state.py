from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    GAME_MODE_CHOOSING = auto()
    LEVEL_CHOOSING = auto()
    PLAY = auto()
    INFINITE_PLAY = auto()
    EDUCATION = auto()
    ACHIEVEMENTS = auto()
    EXIT = auto()
