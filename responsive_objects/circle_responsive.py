import pygame
from responsive_objects.responsive import ResponsiveObject


class RectangleResponsive(ResponsiveObject):
    def __init__(self, cx, cy, radius, *args):
        """Implementation of ResponsiveObject which is addressed when user puts cursor inside
        addressing circle defined by its center position and radius"""
        self._cx = cx
        self._cy = cy
        self._radius = radius
        super().__init__(*args)

    def _is_addressed(self) -> bool:
        x, y = pygame.mouse.get_pos()
        dist_from_center = ((self._cx - x) ** 2 + (self._cy - y) ** 2) ** 0.5
        return dist_from_center <= self._radius
