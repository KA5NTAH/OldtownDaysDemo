from enum import Enum, auto


class LvlStage(Enum):
    USUAL_PLAY = auto()
    CHALLENGE = auto()
    WINNER_OPTIONS = auto()
    LOSER_OPTIONS = auto()
    TRIAL_OF_THE_SEVEN = auto()