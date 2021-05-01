from command import Command
from game_enums.game_state import GameState
from game_enums.achievements_names import AchievementsNames
from navigator import Navigator


class SetAchievementCommand(Command):
    def __init__(self, navigator: Navigator, achievement: AchievementsNames):
        self._navigator = navigator
        self._achievement = achievement

    def execute(self):
        self._navigator.switch_to_state(GameState.ACHIEVEMENT_VIEW)
        self._navigator.set_achievement(self._achievement)
