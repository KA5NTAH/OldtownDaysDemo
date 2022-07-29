from responsive_objects.rectangle_responsive import RectangleResponsive
from responsive_objects.mouse_responsive import MouseResponsive
from game_enums.user_intention import UserIntention
from command import Command
import pygame


class Button(RectangleResponsive, MouseResponsive):
    """Button is mean to represent simple button without additional conditions. It has 2 stages reflected by
    its draw logic:
    1) When cursor is not pointed at button it is drawn in idle state
    2) When cursor is pointed at button it is drawn in ready-to-use (addressing) state"""

    def __init__(
        self, idle_image, addressing_image, position, mouse_button, command: Command
    ):
        # todo rename addressing image with something more appropriate
        self._command = command
        self._idle_image = idle_image
        self._addressing_image = addressing_image
        _, _, w, h = self._idle_image.get_rect()
        self._draw_position = position
        super().__init__(pygame.Rect(*self._draw_position, w, h), mouse_button)

    @property
    def draw_position(self):
        return self._draw_position

    def draw(self, screen):
        if self._is_addressed():
            screen.blit(self._addressing_image, self._draw_position)
        else:
            screen.blit(self._idle_image, self._draw_position)

    def click(self):
        self._command.execute()
