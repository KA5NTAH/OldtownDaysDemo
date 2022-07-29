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
        """In order to avoid decorators like this: @AchievementCheckDict.register method __call__ was overridden"""

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
        super().__init__(config_path)
        self._init_from_file()

    def update_tracking_value(self, value: AchievementTrackingValues, amount: int = 1):
        self._achievement_values_info[value.name] += amount

    def dump_into_file(self):
        with open(self._config_path, "w") as file:
            json.dump(self._achievement_values_info, file)

    def _init_from_file(self):
        if not os.path.exists(self._config_path):
            self.dump_into_file()
        else:
            with open(self._config_path) as file:
                self._achievement_values_info = json.load(file)

    def get_achievements_completeness(self):
        completeness = {}
        for ach_name in AchievementsNames:
            completeness[ach_name] = self.achievement_checker[ach_name](self)
        return completeness

    # gold related
    @achievement_checker(AchievementsNames.I_WILL_KEEP_THAT)
    def _i_will_keep_that(self):
        return (
            self._achievement_values_info[AchievementTrackingValues.COLLECTED_GOLD.name]
            >= 1
        )

    @achievement_checker(AchievementsNames.MASTER_OF_COIN)
    def _master_of_coin(self):
        return (
            self._achievement_values_info[AchievementTrackingValues.COLLECTED_GOLD.name]
            >= 1000
        )

    @achievement_checker(AchievementsNames.LORD_OF_CASTERLY_ROCK)
    def _lord_of_casterly_rock(self):
        return (
            self._achievement_values_info[AchievementTrackingValues.COLLECTED_GOLD.name]
            >= 100000
        )

    @achievement_checker(AchievementsNames.IRON_BANK)
    def _iron_bank(self):
        return (
            self._achievement_values_info[AchievementTrackingValues.COLLECTED_GOLD.name]
            >= 1000000
        )

    # blackfyre gold related
    @achievement_checker(AchievementsNames.CONSOLATION_PRIZE)
    def _consolation_prize(self):
        return (
            self._achievement_values_info[
                AchievementTrackingValues.COLLECTED_BLACKFYRE_COINS.name
            ]
            >= 1
        )

    @achievement_checker(AchievementsNames.BLACK_DRAGON_BANNERMAN)
    def _black_dragon_bannerman(self):
        return (
            self._achievement_values_info[
                AchievementTrackingValues.COLLECTED_BLACKFYRE_COINS.name
            ]
            >= 50
        )

    @achievement_checker(AchievementsNames.THE_KING_WHO_BORE_THE_SWORD)
    def _the_king_who_bore_the_sword(self):
        return (
            self._achievement_values_info[
                AchievementTrackingValues.COLLECTED_BLACKFYRE_COINS.name
            ]
            >= 100
        )

    # trial of the seven
    @achievement_checker(AchievementsNames.GODS_HAVE_MADE_THEIR_WILL_KNOWN)
    def _gods_have_made_their_will_known(self):
        return (
            self._achievement_values_info[
                AchievementTrackingValues.TRAIL_OF_THE_SEVEN_CALLS.name
            ]
            >= 1
        )

    # game progress
    @achievement_checker(AchievementsNames.FIRST_OF_HIS_NAME)
    def _first_of_his_name(self):
        return (
            self._achievement_values_info[
                AchievementTrackingValues.COMPLETED_LEVELS.name
            ]
            >= 1
        )

    # bribes
    @achievement_checker(AchievementsNames.MAN_WITHOUT_HONOR)
    def _man_without_honor(self):
        return (
            self._achievement_values_info[AchievementTrackingValues.GIVEN_BRIBES.name]
            >= 100
        )

    # miscellaneous
    @achievement_checker(AchievementsNames.BEGGAR_KING)
    def _beggar_king(self):
        return (
            self._achievement_values_info[
                AchievementTrackingValues.NEGATIVE_BALANCE.name
            ]
            >= 1
        )

    # challenges
    @achievement_checker(AchievementsNames.SWORD_OF_THE_MORNING)
    def _sword_of_the_morning(self):
        return (
            self._achievement_values_info[
                AchievementTrackingValues.PERFECT_CHALLENGES.name
            ]
            >= 100
        )

    @achievement_checker(AchievementsNames.GROWING_STRONG)
    def _growing_strong(self):
        return (
            self._achievement_values_info[
                AchievementTrackingValues.PERFECT_CHALLENGES.name
            ]
            >= 1
        )

    @achievement_checker(AchievementsNames.WALK_OF_PUNISHMENT)
    def _walk_of_punishment(self):
        return (
            self._achievement_values_info[
                AchievementTrackingValues.RUINED_CHALLENGES.name
            ]
            >= 100
        )
