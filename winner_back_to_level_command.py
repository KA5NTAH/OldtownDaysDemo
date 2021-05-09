from command import Command
from navigator import Navigator


class WinnerBackToLevelCommand(Command):
    def __init__(self, navigator: Navigator):
        self._navigator = navigator

    def execute(self):
        self._navigator.go_back(steps=2)