from command import Command
from navigator import Navigator
from persistent_objects.currencies_manager import CurrenciesManager
from game_enums.lvl_stage import LvlStage
from game_enums.coins_kinds import CoinsKinds


class TrialCommand(Command):
    def __init__(self, navigator: Navigator, currencies_manager: CurrenciesManager, trial_cost):
        self._navigator = navigator
        self._currencies_manager = currencies_manager
        self._trial_cost = trial_cost

    def execute(self):
        self._navigator.switch_to_play_state(LvlStage.GENERATE_TRIAL_RESULT)  # fixme it this relevant
        self._currencies_manager.spend_coins(CoinsKinds.FAITH_COIN, self._trial_cost)
