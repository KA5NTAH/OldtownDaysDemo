import pygame
import os
import sys
import numpy as np
from game_enums.achievements_names import AchievementsNames
from game_enums.user_intention import UserIntention
from responsive_objects.slide import Slide
from responsive_objects.achievement_button import AchievementButton
from responsive_objects.mouse_responsive import MouseResponsive
from game_constants import ACHIEVEMENTS_IMAGES, SCREEN_WIDTH, SCREEN_HEIGHT, ACH_HEIGHT, ACH_WIDTH


# todo delete
class AchievementPanel(MouseResponsive, Slide):
    def __init__(self):
        super().__init__(0)
        # parameters for counting buttons drawing positions
        self._x_offset = 20
        self._y_offset = 20
        self._x_start = 50
        self._y_start = 50
        self._buttons_drawing_positions = self._get_drawing_positions()  # fixme do we need to keep this?
        self._big_icon_active_pos = (200, 175)
        self._description_pos = (447, 175)
        self._buttons = self._init_buttons()
        self._ach_state = self._get_achievements_state(0)  # fixme dummy implementation without achievement manager
        self._spectating_button = -1

    def _get_drawing_positions(self):
        x_stop = SCREEN_WIDTH - ACH_WIDTH - self._x_offset
        x = np.arange(self._x_start, x_stop + 1, ACH_WIDTH + self._x_offset)
        y_stop = SCREEN_HEIGHT - ACH_HEIGHT - self._y_offset
        y = np.arange(self._y_start, y_stop + 1, ACH_HEIGHT + self._y_offset)
        xx, yy = np.meshgrid(x, y)
        coord = np.vstack((xx.flatten(), yy.flatten())).T
        return coord

    def _init_buttons(self):
        """returns list of buttons"""  # fixme kind of obvious do we even need this
        buttons = []
        for index, a in enumerate(AchievementsNames):
            if a in ACHIEVEMENTS_IMAGES.keys():
                button = AchievementButton(a.name,
                                           *ACHIEVEMENTS_IMAGES[a],
                                           self._buttons_drawing_positions[index],
                                           self._big_icon_active_pos,
                                           self._description_pos,
                                           0)
                buttons.append(button)
        return buttons

    # todo later implement interaction with achievement manager
    def _get_achievements_state(self, achievement_manager):
        dummy_dict = {}
        for a in AchievementsNames:
            dummy_dict[a.name] = False
        return dummy_dict

    def update(self):
        """ track which button was pressed and assign it to be spectated:
        it is should be tracked because it is should be drawn last. every mouse pressing menas that whatever 
        button was in spectative mode it should exit it"""   # fixme refine this string
        # if no button is in spectator mode check if some button is pressed
        if self._spectating_button == -1:
            for index, button in enumerate(self._buttons):
                if button.get_user_intention_and_update_track() == UserIntention.SWITCH_ON:
                    self._spectating_button = index
        # else every pressing is considered to be exit out of spectator mod
        else:
            if self.get_user_intention_and_update_track() == UserIntention.SWITCH_ON:
                self._spectating_button = -1

    def draw(self, screen):
        for index, button in enumerate(self._buttons):
            ach_name = button.achievement_name
            button.draw_idle(screen, self._ach_state[ach_name])
        if self._spectating_button != -1:
            ach_name = self._buttons[self._spectating_button].achievement_name
            self._buttons[self._spectating_button].draw_description(screen, self._ach_state[ach_name])


if __name__ == '__main__':
    pygame.init()
    p = AchievementPanel()
    black = (255, 255, 255)
    screen = pygame.display.set_mode((1200, 680))
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(black)
        p.update()
        p.draw(screen)
        pygame.display.flip()
