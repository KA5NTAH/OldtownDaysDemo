from command import Command
from navigator import Navigator
from game_enums.lvl_stage import LvlStage
from game_enums.game_state import GameState


class NextLevelCommand(Command):
    def __init__(self, navigator: Navigator):
        self._navigator = navigator

    def execute(self):
        self._navigator.increment_level()
        self._navigator.switch_to_state(GameState.PLAY)
        self._navigator.switch_to_play_state(LvlStage.USUAL_PLAY)
