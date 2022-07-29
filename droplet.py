import pygame
import sys
import utils
from flyweight_droplet import FlyWeightDroplet
from flywght_droplet_factory import FlyweightDropletFactory
from game_constants import DROPLET_WIDTH, DROPLET_HEIGHT


# todo implement flyweight pattern
class Droplet:
    def __init__(self, metal, y_speed, position):
        self._flyweight = FlyweightDropletFactory.get_flyweight(metal)
        self._y_speed = y_speed
        self._rect = pygame.Rect(*position, DROPLET_WIDTH, DROPLET_HEIGHT)

    @property
    def rect(self):
        return self._rect

    @property
    def metal(self):
        return self._flyweight.metal

    @property
    def y_coord(self):
        return self._rect.top

    def fall(self):
        self._rect = self._rect.move((0, self._y_speed))

    def draw(self, screen):
        self._flyweight.draw(screen, self._rect)
