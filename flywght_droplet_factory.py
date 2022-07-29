from flyweight_droplet import FlyWeightDroplet
from game_enums.metals import Metals


class FlyweightDropletFactory:
    """Flyweight factory is used as in FLyweight pattern in order to reuse shared object states in convenient way"""

    _cache = {}

    @staticmethod
    def get_flyweight(metal):
        return FlyweightDropletFactory._cache.setdefault(metal, FlyWeightDroplet(metal))
