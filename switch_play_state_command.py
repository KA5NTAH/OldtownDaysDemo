from command import Command
from navigator import Navigator
from game_enums.lvl_stage import LvlStage


class SwitchPlayStateCommand(Command):
    def __init__(self, navigator: Navigator, lvl_stage: LvlStage):
        self._navigator = navigator
        self._lvl_stage = lvl_stage

    def execute(self):
        self._navigator.switch_to_play_state(self._lvl_stage)