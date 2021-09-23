from command import Command
from navigator import Navigator


class StateSetbackCommand(Command):
    def __init__(self, navigator: Navigator):
        self._navigator = navigator

    def execute(self):
        self._navigator.go_back()
