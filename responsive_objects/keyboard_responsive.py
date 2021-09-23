import pygame
from responsive_objects.responsive import ResponsiveObject


class KeyboardResponsive(ResponsiveObject):
    def __init__(self, kb_key, *args):
        """Implementation of ResponsiveObject which keeps track of click on certain keyboard button"""
        self._kb_key = kb_key
        super().__init__(*args)

    def _get_user_action(self) -> bool:
        return pygame.key.get_pressed()[self._kb_key]

    def _is_addressed(self):
        return True
