from command import Command
from navigator import Navigator
from game_enums.game_state import GameState


class SwitchStateCommand(Command):
    def __init__(self, navigator: Navigator, dst_state: GameState):
        self._dst_state = dst_state
        self._navigator = navigator

    def execute(self):
        self._navigator.switch_to_state(self._dst_state)
