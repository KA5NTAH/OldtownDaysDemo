from command import Command
from navigator import Navigator
from persistent_objects.currencies_manager import CurrenciesManager
from game_enums.lvl_stage import LvlStage
from game_enums.coins_kinds import CoinsKinds
from game_enums.bonuses import Bonuses
from game_constants import FATHERS_PUNISHMENT


class AcceptTrialResultCommand(Command):
    def __init__(self, navigator: Navigator, currencies_manager: CurrenciesManager, bonus: Bonuses, father_jdgmnt: bool,
                 level):
        self._navigator = navigator
        self._currencies_manager = currencies_manager
        self._bonus = bonus
        self._fathers_judgement = father_jdgmnt
        self._level = level

    def execute(self):
        if self._bonus == Bonuses.MOTHER:
            """ return to the usual play state """
            self._navigator.switch_to_play_state(LvlStage.USUAL_PLAY)
            self._level.activate_events()
        elif self._bonus == Bonuses.FATHER:
            if self._fathers_judgement:
                """ return to the usual play state """
                self._navigator.switch_to_play_state(LvlStage.USUAL_PLAY)
                self._level.activate_events()
            else:
                """ pay the price and return back to menu """
                self._currencies_manager.spend_coins(CoinsKinds.FAITH_COIN, FATHERS_PUNISHMENT)
                self._navigator.go_back()
        else:
            """ set corresponding bonus and return back to menu"""
            self._navigator.set_bonus(self._bonus)
            self._navigator.go_back()