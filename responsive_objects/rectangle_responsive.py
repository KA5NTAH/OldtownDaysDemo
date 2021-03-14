import pygame
from responsive_objects.responsive import ResponsiveObject


class RectangleResponsive(ResponsiveObject):
    """Implementation of ResponsiveObject which is addressed when user puts cursor inside
    addressing rectangle"""
    def __init__(self, adressing_rect, *args):
        self._addressing_rect = adressing_rect
        super().__init__(*args)

    def _is_addressed(self) -> bool:
        x, y = pygame.mouse.get_pos()
        left, top, w, h = self._addressing_rect
        return left <= x <= left + w and top <= y <= top + h
