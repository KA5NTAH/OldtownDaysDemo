from command import Command
from navigator import Navigator
from game_constants import EDUCATION_SLIDES_AMOUNT


class EducationalForwardCommand(Command):
    def __init__(self, navigator: Navigator):
        self._navigator = navigator

    def execute(self):
        if self._navigator.current_education_step + 1 == EDUCATION_SLIDES_AMOUNT:
            self._navigator.current_education_step = 0
            self._navigator.go_back()
        else:
            self._navigator.current_education_step += 1
