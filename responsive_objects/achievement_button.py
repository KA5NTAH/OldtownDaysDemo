from responsive_objects.rectangle_responsive import RectangleResponsive
from responsive_objects.mouse_responsive import MouseResponsive
from game_enums.user_intention import UserIntention
import pygame

# todo delete there is no more need of this
class AchievementButton(RectangleResponsive, MouseResponsive):
    """
    Achievement button represents information about achievement While icon is idle its color can tell whether it is
    unlocked or not, in active state text description is available
    """
    def __init__(self, ach_name, small_icon_locked, small_icon_unlocked, big_icon_locked, big_icon_unlocked, description,
                 small_icon_pos, big_icon_pos, description_pos, mouse_button):
        # todo rename addressing image with something more appropriate
        self._ach_name = ach_name
        self._small_icon_locked = small_icon_locked
        self._small_icon_unlocked = small_icon_unlocked
        self._big_icon_locked = big_icon_locked
        self._big_icon_unlocked = big_icon_unlocked
        self._description = description
        # positions
        self._small_icon_pos = small_icon_pos
        self._big_icon_pos = big_icon_pos
        self._description_pos = description_pos
        _, _, w, h = self._small_icon_locked.get_rect()
        super().__init__(pygame.Rect(*self._small_icon_pos, w, h), mouse_button)

    @property
    def achievement_name(self):
        return self._ach_name

    def draw_idle(self, screen, locked):
        """ Small icon with different images for locked and unlocked achievements """
        if locked:
            screen.blit(self._small_icon_locked, self._small_icon_pos)
        else:
            screen.blit(self._small_icon_unlocked, self._small_icon_pos)

    def draw_description(self, screen, locked):
        """ Draw achievement with text description. Locked and unlocked images have different images"""
        if locked:
            screen.blit(self._big_icon_locked, self._big_icon_pos)
        else:
            screen.blit(self._big_icon_unlocked, self._big_icon_pos)
        screen.blit(self._description, self._description_pos)