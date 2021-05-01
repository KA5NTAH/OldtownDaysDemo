from game_enums.metals import Metals
from game_constants import DROPLETS_IMAGES


class FlyWeightDroplet:
    def __init__(self, metal: Metals):
        self._image = DROPLETS_IMAGES[metal]
        self._metal = metal

    @property
    def metal(self):
        return self._metal

    def draw(self, screen, rect):
        screen.blit(self._image, (rect.left, rect.top))
