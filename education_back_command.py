from command import Command
from navigator import Navigator


class EducationBackCommand(Command):
    def __init__(self, navigator: Navigator):
        self._navigator = navigator

    def execute(self):
        if self._navigator.current_education_step > 0:
            self._navigator.current_education_step -= 1
