from game_enums.game_state import GameState
from game_enums.achievements_names import AchievementsNames
from game_enums.lvl_stage import LvlStage
from game_enums.bonuses import Bonuses


class Navigator:
    def __init__(self):
        self._current_state = GameState.MENU
        self._state_history = [GameState.EXIT]
        """ some states should not be in history """
        self._forbidden_to_be_in_history = [GameState.LEVEL_WINNER_OPTIONS]
        self._play_state_history = []  # fixme is this necessary
        self._played_level = None
        self._current_level_state = LvlStage.USUAL_PLAY
        self._displayed_achievement = None
        self._bonus = None

    @property
    def current_state(self):
        return self._current_state

    @property
    def current_level_state(self):
        return self._current_level_state

    @property
    def displayed_achievement(self):
        return self._displayed_achievement

    @property
    def played_level(self):
        return self._played_level

    def increment_level(self):
        self._played_level += 1

    def switch_to_state(self, dst_state):
        """ do not allow forbidden states and two identical states in a row"""
        if self._current_state not in self._forbidden_to_be_in_history and self._current_state != self._state_history[-1]:
            self._state_history.append(self._current_state)
        # if we left play state its history should be deleted
        if self._current_state == GameState.PLAY:
            self._play_state_history = []
        self._current_state = dst_state
        # if we come into play state lvl should be set into usual play
        if self._current_state == GameState.PLAY:
            self.switch_to_play_state(LvlStage.USUAL_PLAY)

    def switch_to_play_state(self, dst_state):
        self._play_state_history.append(self._current_level_state)
        self._current_level_state = dst_state

    def go_back(self, steps=1):
        if self._current_state == GameState.PLAY:
            self._play_state_history = []
        for step in range(steps):
            self._current_state = self._state_history.pop(-1)

    def set_achievement(self, achievement: AchievementsNames):
        self._displayed_achievement = achievement
    
    def set_level(self, level_num: int):
        self._played_level = level_num

    def set_bonus(self, bonus: Bonuses):
        self._bonus = bonus