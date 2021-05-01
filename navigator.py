from game_enums.game_state import GameState
from game_enums.achievements_names import AchievementsNames


class Navigator:
    def __init__(self):
        self._current_state = GameState.MENU
        self._state_history = [GameState.EXIT]
        self._played_level = None
        self._displayed_achievement = None

    @property
    def current_state(self):
        return self._current_state

    def switch_to_state(self, dst_state):
        self._state_history.append(self._current_state)
        self._current_state = dst_state

    def go_back(self):
        if self._state_history:
            self._current_state = self._state_history.pop(-1)

    def set_achievement(self, achievement: AchievementsNames):
        self._displayed_achievement = achievement
    
    def set_level(self, level_num: int):
        self._played_level = level_num