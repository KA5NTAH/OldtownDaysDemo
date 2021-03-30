from game_enums.bonuses import Bonuses
from expiring_object import ExpiringObject
from game_enums.coins_kinds import CoinsKinds
from game_enums.user_intention import UserIntention
import random as rd
import game_constants


class TrialOfTheSeven(ExpiringObject):
    def __init__(self, waiting_time):
        """
        Trial of the seven generates bonus for user
        Trial consists of two parts:
        1) show random bonuses for waiting time
        2) present user with result (if need be executes)
         and give him button to continue at this stage user has 2 options:
            - returns to play state
            - returns to lvl panel
        """
        super().__init__(waiting_time)
        self._time_per_god = 1000
        self._current_god = rd.choice(list(Bonuses))
        self._showed_gods = 0
        self._result_is_generated = False
        self._result_bonus = None
        self._image_with_description = None
        self._back_to_play_button, self._exit_button = self._init_buttons()

    def _init_buttons(self):
        # todo init buttons
        return (1, 1)

    def update(self, level_progress, currencies_manager):
        """

        """
        self.update_ttl()
        if self.is_still_alive():
            # generate current god if old time is gone
            spent_time = self._life_time - self._ttl
            if spent_time // self._time_per_god > self._showed_gods:
                self._showed_gods += 1
                self._current_god = rd.choice(list(Bonuses))
        else:
            if not self._result_is_generated:
                self._result_bonus = rd.choice(list(Bonuses))
                self._result_is_generated = True
                if self._result_bonus == Bonuses.FATHER:
                    if level_progress >= game_constants.FATHERS_JUDGEMENT_THRD:
                        currencies_manager.spend_coins(CoinsKinds.FAITH_COIN, game_constants.FATHERS_PUNISHMENT)
                        self._image_with_description = 0
                    else:
                        self._image_with_description = 1
                else:
                    self._image_with_description = 2
            else:
                if self._result_bonus == Bonuses.MOTHER:
                    user_intention = self._back_to_play_button.get_user_intention_and_update_track()
                else:
                    user_intention = self._exit_button.get_user_intention_and_update_track()
                if user_intention == UserIntention.SWITCH_ON:
                    return True
                return None

    def draw(self, screen):
        if self.is_still_alive():
            god_image = 0  # todo in game_constants add dict with gods images
            screen.blit(god_image)
        elif self._result_is_generated:
            # todo
            screen.blit()

    def run_trial(self, screen):
        result_bonus = rd.choice(list(Bonuses))
        user_returns_to_play_state = None


