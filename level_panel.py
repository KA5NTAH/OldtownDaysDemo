from responsive_objects.lvl_button import LvlButton
from game_constants import SCREEN_WIDTH, SCREEN_HEIGHT, LVL_BUTTONS_IMAGES, LVL_ICON_HEIGHT, LVL_ICON_WIDTH, MOUSE_KEY
import pygame
import numpy as np
from game_enums.user_intention import UserIntention


class LevelPanel:
    def __init__(self):
        self._x_offset = 20
        self._y_offset = 20
        self._x_start = 50
        self._y_start = 50
        self._buttons = self._init_buttons()
        self._buttons_num = len(self._buttons)

    def _get_drawing_positions(self):
        # fixme violation of DRY mb put this method into utils?
        x_stop = SCREEN_WIDTH - LVL_ICON_WIDTH - self._x_offset
        x = np.arange(self._x_start, x_stop + 1, LVL_ICON_WIDTH + self._x_offset)
        y_stop = SCREEN_HEIGHT - LVL_ICON_HEIGHT - self._y_offset
        y = np.arange(self._y_start, y_stop + 1, LVL_ICON_HEIGHT + self._y_offset)
        xx, yy = np.meshgrid(x, y)
        coord = np.vstack((xx.flatten(), yy.flatten())).T
        print(coord)
        return coord

    def _init_buttons(self):
        positions = self._get_drawing_positions()
        buttons = []
        for index, images in enumerate(LVL_BUTTONS_IMAGES):
            button = LvlButton(*images, positions[index], MOUSE_KEY)
            buttons.append(button)
        return buttons

    def update_and_return_selected_lvl(self):
        selected_index = None
        for index, b_ind in enumerate(range(self._buttons_num)):
            intention = self._buttons[b_ind].get_user_intention_and_update_track()
            if intention == UserIntention.SWITCH_ON:
                selected_index = index
        return selected_index

    def draw(self, screen, locked_states):
        # todo draw some bacground
        for button, locked in zip(self._buttons, locked_states):
            button.draw(screen, locked)


if __name__ == '__main__':
    pygame.init()
    p = LevelPanel()
    black = (255, 255, 255)
    screen = pygame.display.set_mode((1200, 680))
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(black)
        res = p.update_and_return_selected_lvl()
        if res is not None:
            print(res)
        p.draw(screen, [i > 5 for i in range(15)])
        pygame.display.flip()