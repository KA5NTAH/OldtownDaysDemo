import pygame
import sys
from responsive_objects.circle_responsive import CircleResponsive
from responsive_objects.mouse_responsive import MouseResponsive

GOLD = (255, 215, 0)
BLEAK = (15, 15, 15)


class ChallengeTarget(CircleResponsive, MouseResponsive):
    # todo idk rename or something
    def __init__(
        self, trace_image, idle_image, calling_image, cx, cy, radius, mouse_key
    ):
        self._trace_image = trace_image
        self._idle_image = idle_image
        self._calling_image = calling_image
        # define drawing position i.e. left top position corresponding to center
        _, _, w, h = trace_image.get_rect()
        super().__init__(cx, cy, radius, mouse_key)
        self._drawing_position = (self._cx - int(w // 2), self._cy - int(h // 2))

    def set_new_center(self, new_cx, new_cy):
        self._cx = new_cx
        self._cy = new_cy
        self._drawing_position = (self._cx - self._radius, self._cy - self._radius)

    def draw_trace(self, screen):
        screen.blit(self._trace_image, self._drawing_position)

    def draw_idle(self, screen):
        screen.blit(self._idle_image, self._drawing_position)

    def draw_calling(self, screen):
        screen.blit(self._calling_image, self._drawing_position)
