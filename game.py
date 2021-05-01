from enum import Enum, auto
import pygame
from game_enums.game_state import GameState
from game_enums.bonuses import Bonuses
from responsive_objects.button import Button
import sys
import os
import game_constants
from navigator import Navigator
from game_enums.user_intention import UserIntention
from switch_state_command import SwitchStateCommand


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode((game_constants.SCREEN_WIDTH, game_constants.SCREEN_HEIGHT))
        self._state = GameState.GAME_MODE_CHOOSING
        self._navigator = Navigator()
        self._menu_bg = game_constants.MENU_BACKGROUND
        self._mode_choosing_bg = game_constants.MODE_SELECTION_BACKGROUND
        self._menu_buttons = self._init_menu_buttons()
        self._game_choosing_buttons = self._init_game_choosing_buttons()
        self._level_buttons = self._init_level_buttons()

    def _process_buttons(self, buttons):
        for index in range(len(buttons)):
            user_intention = buttons[index].get_user_intention_and_update_track()
            if user_intention == UserIntention.SWITCH_OFF:
                buttons[index].click()

    def _draw_buttons(self, buttons, screen):
        for b in buttons:
            b.draw(screen)

    def _init_achievement_buttons(self):
        return [], []

    # approved
    def _init_menu_buttons(self):
        menu_buttons = []
        for button_info in game_constants.MENU_BUTTONS_INFO:
            # def __init__(self, idle_image, addressing_image, position, mouse_button, command: Command):
            images = button_info["images"]
            position = button_info["position"]
            dst_state = button_info["state"]
            command = SwitchStateCommand(self._navigator, dst_state)
            button = Button(*images, position, game_constants.MOUSE_KEY, command)
            menu_buttons.append(button)
        return menu_buttons

    # approved
    def _init_game_choosing_buttons(self):
        game_choosing_buttons = []
        for button_info in game_constants.MODE_SELECTION_BUTTONS_INFO:
            images = button_info["images"]
            position = button_info["position"]
            dst_state = button_info["state"]
            command = SwitchStateCommand(self._navigator, dst_state)
            button = Button(*images, position, game_constants.MOUSE_KEY, command)
            game_choosing_buttons.append(button)
        return game_choosing_buttons

    def _init_achievement_buttons(self):
        return []

    def _init_level_buttons(self):
        return []

    def _init_levels(self):
        return []

    def update(self):
        # detect back command
        if self._navigator.current_state == GameState.MENU:
            self._process_buttons(self._menu_buttons)
        if self._navigator.current_state == GameState.GAME_MODE_CHOOSING:
            self._process_buttons(self._game_choosing_buttons)
        if self._navigator.current_state == GameState.LEVEL_CHOOSING:
            self._process_buttons(self._level_buttons)

    def draw(self, screen):
        if self._navigator.current_state == GameState.MENU:
            screen.blit(self._menu_bg, (0, 0))
            self._draw_buttons(self._menu_buttons, screen)
        if self._navigator.current_state == GameState.GAME_MODE_CHOOSING:
            screen.blit(self._mode_choosing_bg, (0, 0))
            self._draw_buttons(self._game_choosing_buttons, screen)
        if self._navigator.current_state == GameState.LEVEL_CHOOSING:
            # todo add locked/unlocked logic
            self._draw_buttons(self._level_buttons, screen)
        if self._navigator.current_state == GameState.PLAY:
            pass
        if self._navigator.current_state == GameState.ACHIEVEMENT_VIEW:
            # todo draw achievement
            pass

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
