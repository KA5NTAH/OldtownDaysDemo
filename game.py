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
from set_achievement_command import SetAchievementCommand
from achievement_manager import AchievementManager
from persistent_objects.currencies_manager import CurrenciesManager
from responsive_objects.keyboard_responsive import KeyboardResponsive


# fixme completness should be taken only once player enters achievement window NOW it is taken on every frame


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode((game_constants.SCREEN_WIDTH, game_constants.SCREEN_HEIGHT))
        self._state = GameState.GAME_MODE_CHOOSING
        self._navigator = Navigator()
        self._menu_bg = game_constants.MENU_BACKGROUND
        self._mode_choosing_bg = game_constants.MODE_SELECTION_BACKGROUND
        self._menu_buttons = self._init_menu_buttons()
        self._game_choosing_buttons = self._init_game_choosing_buttons()
        self._achievements_info = self._init_achievements_info()
        self._level_buttons = self._init_level_buttons()
        self._achievement_manager = AchievementManager(game_constants.ACHIEVEMENTS_INFO)
        self._currencies_manager = CurrenciesManager(game_constants.CURRENCIES_INFO)
        # keep track of escape button
        self._roll_back_button = KeyboardResponsive(pygame.K_ESCAPE)

    def _process_buttons(self, buttons):
        for index in range(len(buttons)):
            user_intention = buttons[index].get_user_intention_and_update_track()
            if user_intention == UserIntention.SWITCH_OFF:
                buttons[index].click()

    def _draw_buttons(self, buttons, screen):
        for b in buttons:
            b.draw(screen)

    def _draw_achievement_buttons(self, screen):
        completeness_map = self._achievement_manager.get_achievements_completeness()
        for key in completeness_map.keys():
            # fixme delete later needed because not all images are ready
            if key not in self._achievements_info:
                continue
            if completeness_map[key]:
                self._achievements_info[key]["unlocked_button"].draw(screen)
            else:
                self._achievements_info[key]["locked_button"].draw(screen)

    def _display_achievement(self, screen, ach_name):
        completeness_map = self._achievement_manager.get_achievements_completeness()
        screen.blit(self._achievements_info[ach_name]["description"], game_constants.ACHIEVEMENT_DESCRIPTION_POS)
        if completeness_map[self._navigator.displayed_achievement]:
            screen.blit(self._achievements_info[ach_name]["unlocked_icon"], game_constants.ACHIEVEMENT_ICON_POS)
        else:
            screen.blit(self._achievements_info[ach_name]["locked_icon"], game_constants.ACHIEVEMENT_ICON_POS)

    def _process_achievements_buttons(self):
        completeness_map = self._achievement_manager.get_achievements_completeness()
        for key in completeness_map.keys():
            # fixme delete later needed because not all images are ready
            if key not in self._achievements_info:
                continue
            if completeness_map[key]:
                user_intention = self._achievements_info[key]["unlocked_button"].get_user_intention_and_update_track()
                if user_intention == UserIntention.SWITCH_OFF:
                    self._achievements_info[key]["unlocked_button"].click()
            else:
                user_intention = self._achievements_info[key]["locked_button"].get_user_intention_and_update_track()
                if user_intention == UserIntention.SWITCH_OFF:
                    self._achievements_info[key]["locked_button"].click()

    def _init_achievements_info(self):
        # split images into buttons
        achievements_info = {}
        for key, pos in zip(game_constants.ACHIEVEMENTS_IMAGES.keys(), game_constants.ACHIEVEMENT_POSITIONS):
            small_icon_locked, small_icon_unlocked, \
                               big_icon_locked, big_icon_unlocked, description = game_constants.ACHIEVEMENTS_IMAGES[key]
            command = SetAchievementCommand(self._navigator, key)
            locked_button = Button(small_icon_locked, small_icon_locked, pos, game_constants.MOUSE_KEY, command)
            unlocked_button = Button(small_icon_unlocked, small_icon_unlocked, pos, game_constants.MOUSE_KEY, command)
            achievement_info = {"locked_button": locked_button,
                                "unlocked_button": unlocked_button,
                                "locked_icon": big_icon_locked,
                                "unlocked_icon": big_icon_unlocked,
                                "description": description}
            achievements_info[key] = achievement_info
        return achievements_info

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

    def _init_level_buttons(self):
        return []

    def _init_levels(self):
        return []

    def update(self):
        # detect escape command
        go_back = self._roll_back_button.get_user_intention_and_update_track() == UserIntention.SWITCH_OFF
        if go_back:
            self._navigator.go_back()
        # update corresponding to current state
        if self._navigator.current_state == GameState.MENU:
            self._process_buttons(self._menu_buttons)
        if self._navigator.current_state == GameState.GAME_MODE_CHOOSING:
            self._process_buttons(self._game_choosing_buttons)
        if self._navigator.current_state == GameState.LEVEL_CHOOSING:
            self._process_buttons(self._level_buttons)
        if self._navigator.current_state == GameState.ACHIEVEMENTS:
            self._process_achievements_buttons()
        if self._navigator.current_state == GameState.EXIT:
            sys.exit()

    def draw(self, screen):
        if self._navigator.current_state == GameState.MENU:
            screen.blit(self._menu_bg, (0, 0))
            self._draw_buttons(self._menu_buttons, screen)
        if self._navigator.current_state == GameState.GAME_MODE_CHOOSING:
            screen.blit(self._mode_choosing_bg, (0, 0))
            self._draw_buttons(self._game_choosing_buttons, screen)
        if self._navigator.current_state == GameState.LEVEL_CHOOSING:
            self._draw_buttons(self._level_buttons, screen)
        if self._navigator.current_state == GameState.ACHIEVEMENTS:
            self._draw_achievement_buttons(screen)
        if self._navigator.current_state == GameState.ACHIEVEMENT_VIEW:
            ach_name = self._navigator.displayed_achievement
            self._display_achievement(screen, ach_name)

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
