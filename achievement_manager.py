import json
import os
from persistent_objects.persistent_object import PersistentObject
from game_enums.achievements_names import AchievementsNames
from game_enums.achievement_tracking_values import AchievementTrackingValues


class AchievementCheckDict(dict):
    """
    Special implementation of dictionary for storing info about achievement progress
    for each achievement name there is stored method of AchievementManager class that counts achievement state
    In order to not write all association in dict manually this implementation provides decorator that automatically
    does association with given achievement name
    """
    def __call__(self, achievement_name):
        def decorator(foo):
            self.__setitem__(achievement_name, foo)
            return foo
        return decorator


class AchievementManager(PersistentObject):
    """Achievement manager is responsible for tracking achievements states
        It is done with the help of 2 dicts:
        1) First keeps track of all values that can influence achievement This one is persistent
        2) Second for every achievement contains function that check achievement completeness based on first dict
    """
    achievement_checker = AchievementCheckDict()

    def __init__(self, config_path):
        values_names = [v.name for v in AchievementTrackingValues]
        self._achievement_values_info = dict.fromkeys(values_names, 0)
        self._achievement_progress_info = dict.fromkeys(list(AchievementsNames), False)
        # self._init_from_file()
        super().__init__(config_path)

    def update_tracking_value(self, value: AchievementTrackingValues, amount: int = 1):
        self._achievement_values_info[value] += amount

    def dump_into_file(self):
        with open(self._config_path, 'w') as file:
            json.dump(self._achievement_values_info, file)

    def _init_from_file(self):
        if not os.path.exists(self._config_path):
            self.dump_into_file()
        else:
            with open(self._config_path) as file:
                self._achievement_values_info = json.load(file)

    # gold related
    @achievement_checker(AchievementsNames.I_WILL_KEEP_THAT)
    def _i_will_keep_that(self):
        return self._achievement_values_info[AchievementTrackingValues.COLLECTED_GOLD] >= 1

    @achievement_checker(AchievementsNames.MASTER_OF_COIN)
    def _master_of_coin(self):
        return self._achievement_values_info[AchievementTrackingValues.COLLECTED_GOLD] >= 1000

    @achievement_checker(AchievementsNames.LORD_OF_CASTERLY_ROCK)
    def _lord_of_casterly_rock(self):
        return self._achievement_values_info[AchievementTrackingValues.COLLECTED_GOLD.name] >= 100000

    @achievement_checker(AchievementsNames.IRON_BANK)
    def _iron_bank(self):
        return self._achievement_values_info[AchievementTrackingValues.COLLECTED_GOLD] >= 1000000

    # blackfyre gold related
    @achievement_checker(AchievementsNames.CONSOLATION_PRIZE)
    def _consolation_prize(self):
        return self._achievement_values_info[AchievementTrackingValues.COLLECTED_BLACKFYRE_COINS] >= 1

    @achievement_checker(AchievementsNames.BLACK_DRAGON_BANNERMAN)
    def _black_dragon_bannerman(self):
        return self._achievement_values_info[AchievementTrackingValues.COLLECTED_BLACKFYRE_COINS] >= 50

    @achievement_checker(AchievementsNames.THE_KING_WHO_BORE_THE_SWORD)
    def _the_king_who_bore_the_sword(self):
        return self._achievement_values_info[AchievementTrackingValues.COLLECTED_BLACKFYRE_COINS] >= 100

    # trial of the seven
    @achievement_checker(AchievementsNames.GODS_HAVE_MADE_THEIR_WILL_KNOWN)
    def _gods_have_made_their_will_known(self):
        return self._achievement_values_info[AchievementTrackingValues.TRAIL_OF_THE_SEVEN_CALLS] >= 1

    # game progress
    @achievement_checker(AchievementsNames.FIRST_OF_HIS_NAME)
    def _first_of_his_name(self):
        return self._achievement_values_info[AchievementTrackingValues.COMPLETED_LEVELS] >= 1

    # bribes
    @achievement_checker(AchievementsNames.MAN_WITHOUT_HONOR)
    def _man_without_honor(self):
        return self._achievement_values_info[AchievementTrackingValues.GIVEN_BRIBES] >= 100

    # miscellaneous
    @achievement_checker(AchievementsNames.BEGGAR_KING)
    def _beggar_king(self):
        return self._achievement_values_info[AchievementTrackingValues.NEGATIVE_BALANCE] >= 0


a = AchievementManager("")
print(a.achievement_checker)
