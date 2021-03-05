from enum import Enum, auto


class TargetPressingState(Enum):
    GOT_PRESSED = auto()
    LONG_TIME_PRESSED = auto()
    GOT_RELEASED = auto()
    NOT_PRESSED = auto()