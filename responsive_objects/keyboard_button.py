import pygame
from responsive_objects.keyboard_responsive import KeyboardResponsive
from command import Command


class KeyboardButton(KeyboardResponsive):
    def __init__(self, kb_key, command: Command):
        self._command = command
        super().__init__(kb_key)

    def click(self):
        self._command.execute()
