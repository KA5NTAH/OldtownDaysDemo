import pygame
from responsive_objects.responsive import ResponsiveObject


class MouseResponsive(ResponsiveObject):
    """Implementation of ResponsiveObject which keeps track of click on certain mouse button"""
    def __init__(self, mouse_key, *args):
        self._mouse_key = mouse_key
        super().__init__(*args)

    def _get_user_action(self) -> bool:
        return pygame.mouse.get_pressed()[self._mouse_key]
