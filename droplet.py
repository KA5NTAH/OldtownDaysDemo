import pygame
import sys
import utils


class Droplet:
    def __init__(self, metal, y_speed, img, position):
        self._metal = metal
        self._y_speed = y_speed
        self._img = img  # todo might be we could use some animation
        # todo set constant just for now
        _, _, w, h = img.get_rect()
        self._rect = pygame.Rect(*position, w, h)

    @property
    def rect(self):
        return self._rect

    @property
    def metal(self):
        return self._metal

    @property
    def y_coord(self):
        return self._rect.top

    def fall(self):
        self._rect = self._rect.move((0, self._y_speed))

    def draw(self, screen):
        screen.blit(self._img, (self._rect.left, self._rect.top))

