from command import Command
from navigator import Navigator
from game_enums.game_state import GameState
from game_enums.lvl_stage import LvlStage


class SetLevelCommand(Command):
    def __init__(self, navigator: Navigator, level_num: int):
        self._navigator = navigator
        self._level_num = level_num

    def execute(self):
        self._navigator.switch_to_state(GameState.PLAY)
        self._navigator.set_level(self._level_num)
