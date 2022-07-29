from enum import Enum, auto


# todo complete
class AchievementsNames(Enum):
    # gold related
    I_WILL_KEEP_THAT = auto()  # 1 coin  (мне это пригодится)
    MASTER_OF_COIN = auto()  # 1000 coins
    LORD_OF_CASTERLY_ROCK = auto()  # 100.000 coins
    IRON_BANK = auto()  # 1.000.000 coins
    # lvl related
    FIRST_OF_HIS_NAME = auto()  # 1 lvl
    # blackfyre gold related
    CONSOLATION_PRIZE = auto()  # 1 bf coin
    BLACK_DRAGON_BANNERMAN = auto()  # 50 bf coins
    THE_KING_WHO_BORE_THE_SWORD = auto()  # 100 bf coins
    # challenges
    # todo achievement for 1 perfect challenge
    SWORD_OF_THE_MORNING = auto()  # 100 perfect challenges
    GROWING_STRONG = auto()  # 1 perfect challenge вырастая - крепнем
    WALK_OF_PUNISHMENT = auto()  # ruin 100 challenges  (стезя страданий)
    # trial of the seven related
    GODS_HAVE_MADE_THEIR_WILL_KNOWN = auto()  # 1 trial of the seven call
    # bribes
    MAN_WITHOUT_HONOR = auto()  # 100 bribes
    # miscellaneous
    BEGGAR_KING = (
        auto()
    )  # negative balance fixme mb flea_bottom_scum or smth flea bottom related?
