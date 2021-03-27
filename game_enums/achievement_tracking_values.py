from enum import Enum, auto


class AchievementTrackingValues(Enum):
    # COLLECTION ACHIEVEMENTS
    COLLECTED_GOLD = auto()
    COLLECTED_FAITH_COINS = auto()
    COLLECTED_BLACKFYRE_COINS = auto()
    NEGATIVE_BALANCE = auto()
    # GAME PROGRESS
    COMPLETED_LEVELS = auto()
    # MISC
    GIVEN_BRIBES = auto()
    RUINED_DROPS = auto()
    # CHALLENGES
    RUINED_CHALLENGES = auto()
    COMPLETED_CHALLENGES = auto()
    MISSES_IN_CHALLENGE = auto()
    PERFECT_CHALLENGES = auto()
    # TRIAL OF THE SEVEN ACHIEVEMENTS
    TRAIL_OF_THE_SEVEN_CALLS = auto()
    MOTHERS_MERCY = auto()
    CRONES_WISDOM = auto()
    FATHERS_JUDGEMENT = auto()
    WARRIORS_COURAGE = auto()
