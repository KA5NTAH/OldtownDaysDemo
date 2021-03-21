from enum import Enum, auto


class AchievementTrackingValues(Enum):
    # COLLECTION ACHIEVEMENTS
    COLLECTED_GOLD_COINS = auto()
    COLLECTED_FAITH_COINS = auto()
    COLLECTED_BLACKFYRE_COINS = auto()
    NEGATIVE_BALANCE = auto()
    # GAME PROGRESS
    COMPLETED_LEVELS = auto()
    GIVEN_BRIBES = auto()
    TRAIL_OF_THE_SEVEN_CALLS = auto()
    RUINED_DROPS = auto()
    RUINED_CHALLENGES = auto()
    MISSES_IN_CHALLENGE = auto()
    PERFECT_CHALLENGES = auto()
    # TRIAL OF THE SEVEN ACHIEVEMENTS
    MOTHERS_MERCY = auto()
    CRONES_WISDOM = auto()
    FATHERS_JUDGEMENT = auto()
    WARRIORS_COURAGE = auto()
    COLLECTED_GOLD = auto()
