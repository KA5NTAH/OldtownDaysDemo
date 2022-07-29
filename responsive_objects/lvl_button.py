from game_enums.user_intention import UserIntention
from responsive_objects.rectangle_responsive import RectangleResponsive
from responsive_objects.mouse_responsive import MouseResponsive
import pygame


# todo delete
class LvlButton(RectangleResponsive, MouseResponsive):
    """Lvl Button is meant to lead to Level Play mode from level panel. Lvl button states are:
    1) Locked: locked image is drawn independent of user's actions
    2) Unlocked: Draw idle state image if cursor is not pointed at it, addressing state otherwise"""

    def __init__(
        self, locked_image, idle_image, addressing_image, position, mouse_button
    ):
        self._locked_image = locked_image
        self._idle_image = idle_image
        self._addressing_image = addressing_image
        _, _, w, h = self._idle_image.get_rect()
        self._draw_position = position
        super().__init__(pygame.Rect(*self._draw_position, w, h), mouse_button)

    def draw(self, screen, locked):
        if locked:
            screen.blit(self._locked_image, self._draw_position)
        else:
            if self._is_addressed():
                screen.blit(self._addressing_image, self._draw_position)
            else:
                screen.blit(self._idle_image, self._draw_position)
