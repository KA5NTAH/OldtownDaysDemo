from persistent_objects.persistent_object import PersistentObject
from game_enums.coins_kinds import CoinsKinds
import json
import os


class CurrenciesManager(PersistentObject):
    """Class is responsible for storing info about currencies throughout all game sessions"""
    def __init__(self, config_path):
        super().__init__(config_path)
        self._currencies_info = {CoinsKinds.TARGARYEN_COIN.name: 0,
                                 CoinsKinds.FAITH_COIN.name: 0}
        self._init_from_file()

    @property
    def targ_coins(self):
        return self._currencies_info[CoinsKinds.TARGARYEN_COIN.name]

    @property
    def faith_coins(self):
        return self._currencies_info[CoinsKinds.FAITH_COIN.name]

    def dump_into_file(self) -> None:
        with open(self._config_path, 'w') as file:
            json.dump(self._currencies_info, file)

    def spend_coins(self, coin_kind, amount) -> None:
        self._currencies_info[coin_kind.name] -= amount
        self.dump_into_file()

    def record_coin_pick(self, coin_kind: CoinsKinds) -> None:
        self._currencies_info[coin_kind.name] += 1
        self.dump_into_file()

    def _init_from_file(self) -> None:
        if not os.path.exists(self._config_path):
            self.dump_into_file()
        else:
            with open(self._config_path) as file:
                self._currencies_info = json.load(file)


path = os.path.join('C:\\Users\\ААА\\Desktop\\OldtownDays\\resourses\\configs', 'test.json')
test = CurrenciesManager(path)