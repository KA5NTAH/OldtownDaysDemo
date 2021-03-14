from enum import Enum, auto


class UserIntention(Enum):
    SWITCH_ON = auto()
    KEEP_ON_STATE = auto()  # fixme rename this
    SWITCH_OFF = auto()
    IGNORE = auto()
