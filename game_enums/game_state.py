from enum import Enum, auto


# integrate lvl state into play state. 2 states classes seem redundant
class GameState(Enum):
    MENU = auto()
    GAME_MODE_CHOOSING = auto()
    LEVEL_CHOOSING = auto()
    PLAY = auto()
    INFINITE_PLAY = auto()
    EDUCATION = auto()
    ACHIEVEMENTS = auto()
    ACHIEVEMENT_VIEW = auto()
    EXIT = auto()
    # lvl state
    USUAL_PLAY = auto()
    CHALLENGE = auto()
    WINNER_OPTIONS = auto()
    LOSER_OPTIONS = auto()
    TRIAL_OF_THE_SEVEN = auto()