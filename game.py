from enum import Enum, auto
from education import Education
import pygame
from game_enums.game_state import GameState
from state_switcher import StateSwitcher
from level_panel import LevelPanel
from achievement_panel import AchievementPanel
from game_enums.bonuses import Bonuses
from responsive_objects.button import Button
import sys
import os
import game_constants


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode((game_constants.SCREEN_WIDTH, game_constants.SCREEN_HEIGHT))
        self._state = GameState.GAME_MODE_CHOOSING
        self._menu = self._init_menu()
        self._game_mode_selector = self._init_game_mode_selector()
        self._education = self._init_education()
        self._level_panel = LevelPanel()
        self._levels = self._init_levels()
        self._selected_level_ind = None
        self._achievement_panel = AchievementPanel()

    def _init_menu(self):
        buttons = []
        states = []
        menu = StateSwitcher(buttons, states)
        return menu

    def _init_game_mode_selector(self):
        buttons = []
        states = []
        for state, button_info in game_constants.MODE_SELECTION_BUTTONS_INFO.items():
            states.append(state)
            button = Button(*button_info["images"], button_info["position"], game_constants.MOUSE_KEY)
            buttons.append(button)
        game_mode_selector = StateSwitcher(buttons, states)
        return game_mode_selector

    def _init_education(self):
        return 1

    def _init_levels(self):
        levels = []
        return levels

    def update(self):
        if self._state == GameState.MENU:
            dst_state = self._menu.update_and_returned_selected_state()
            if dst_state is not None:
                self._state = dst_state
        elif self._state == GameState.GAME_MODE_CHOOSING:
            dst_state = self._game_mode_selector.update_and_returned_selected_state()
            if dst_state is not None:
                self._state = dst_state
        elif self._state == GameState.LEVEL_CHOOSING:
            level_num = self._level_panel.update_and_return_selected_lvl()
            if level_num is not None:
                # fixme perhaps there progress should be nullified
                self._selected_level_ind = level_num
                self._state = GameState.PLAY
        elif self._state == GameState.PLAY:
            self._levels[self._selected_level_ind].update()

    def draw(self, screen):
        if self._state == GameState.MENU:
            self._menu.draw(screen)
        elif self._state == GameState.GAME_MODE_CHOOSING:
            self._game_mode_selector.draw(screen)
        elif self._state == GameState.LEVEL_CHOOSING:
            self._level_panel.draw(screen, [i > 0 for i in range(15)])

    def run(self):
        while True:
            events = pygame.event.get((pygame.QUIT,))
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            self._screen.fill((255, 255, 255))
            self.update()
            self.draw(self._screen)
            pygame.display.flip()


app = Game()
app.run()
