from enum import Enum, auto

class GameState(Enum):
    MENU = auto()
    PLAY = auto()  # todo maybe more states for play
    EDUCATION = auto()
    ACHIEVEMENTS = auto()
    SETTINGS = auto()
    EXIT = auto()