import pygame
from challenge_target import ChallengeTarget
from expiring_object import ExpiringObject
from game_enums.user_intention import UserIntention
import game_constants
from collections import deque
from responsive_objects.slide import Slide
from responsive_objects.mouse_responsive import MouseResponsive
from achievement_manager import AchievementManager
from game_enums.achievement_tracking_values import AchievementTrackingValues
import random
import numpy as np
import sys

pygame.font.init()


GOLD = (255, 215, 0)


class Challenge(MouseResponsive, Slide, ExpiringObject):
    """
    Player's task is to activate (i.e. click on them following certain order) all challenge target in time
    If player misses or breaks order then he must start again If he does not meet time ends challenge is not considered
    completed
    """
    def __init__(self, targets_coordinates, metal, time, timer_color, mouse_key):
        super().__init__(mouse_key)
        ExpiringObject.__init__(self, time)
        self._metal = metal
        self._bg_image = game_constants.CHALLENGE_IMAGES[self._metal]['bg_img']
        self._targets_coordinates = targets_coordinates
        self._targets = self._init_targets()
        self._current_target_ind = 0
        self._targets_num = len(self._targets_coordinates)
        self._timer_color = timer_color
        self._perfect = True

    def _init_targets(self):
        targets = []
        for num, coord in enumerate(self._targets_coordinates):
            images = game_constants.CHALLENGE_IMAGES[self._metal]['targets_images'][num]
            target = ChallengeTarget(*images, *coord, game_constants.CHALLENGE_TARGET_RADIUS, self._mouse_key)
            targets.append(target)
        return targets

    def shuffle_targets(self):
        # shuffle indexes
        coordinates = self._targets_coordinates.copy()
        random.shuffle(coordinates)
        for num, coord in enumerate(coordinates):
            self._targets[num].set_new_center(*coord)

    def draw(self, screen):
        screen.blit(self._bg_image, (0, 0))
        # draw time track
        timer_line_len = game_constants.SCREEN_WIDTH * (self._ttl / self._life_time)
        pygame.draw.line(screen, self._timer_color, (0, 0), (0 + int(timer_line_len), 0),
                         game_constants.CHALLENGE_TIMER_LINE_WIDTH)
        # draw all targets
        for num, target in enumerate(self._targets):
            if num < self._current_target_ind:
                target.draw_trace(screen)
            elif num == self._current_target_ind:
                target.draw_calling(screen)
            else:
                target.draw_idle(screen)

    def _handle_miss(self, achievement_manager):
        # reset progress and notify achievement manager
        self._current_target_ind = 0
        self._perfect = False
        achievement_manager.update_tracking_value(AchievementTrackingValues.MISSES_IN_CHALLENGE)

    def update_and_return_result(self, achievement_manager):
        # check if some target was pressed
        if self._current_target_ind == self._targets_num:
            # successful complete of challenge
            if self._perfect:
                achievement_manager.update_tracking_value(AchievementTrackingValues.PERFECT_CHALLENGES)
            achievement_manager.update_tracking_value(AchievementTrackingValues.COMPLETED_CHALLENGES)
            return True
        if not self.is_still_alive() and self._current_target_ind < self._targets_num:
            achievement_manager.update_tracking_value(AchievementTrackingValues.RUINED_CHALLENGES)
            return False  # means fail

        slide_intention = self.get_user_intention_and_update_track()
        user_actions = [self._targets[i].get_user_intention_and_update_track() for i in range(len(self._targets))]
        for num, action in enumerate(user_actions):
            if action == UserIntention.SWITCH_ON:
                if num == self._current_target_ind:
                    self._current_target_ind += 1
                else:
                    self._handle_miss(achievement_manager)
                break
        else:
            # check slide click only if no challenge target was pressed
            if slide_intention == UserIntention.SWITCH_ON:
                self._handle_miss(achievement_manager)
        self.update_ttl()


if __name__ == '__main__':
    pygame.init()
    ccord = [[100, 100],
             [500, 200],
             [900, 100],
             [1000, 500],
             [100, 600]]
    from game_enums.metals import Metals
    c = Challenge(ccord, Metals.GOLD, 10000, (255, 0, 0), 0)
    c.shuffle_targets()
    screen = pygame.display.set_mode((1280, 680))
    am = AchievementManager("")
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((255, 255, 255))
        # update block
        c.update_and_return_result(am)
        # draw block
        c.draw(screen)
        pygame.display.flip()