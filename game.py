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
from set_level_command import SetLevelCommand
from achievement_manager import AchievementManager
from persistent_objects.currencies_manager import CurrenciesManager
from responsive_objects.keyboard_responsive import KeyboardResponsive
from bribe_command import BribeCommand
from trial_command import TrialCommand
from switch_play_state_command import SwitchPlayStateCommand
from game_enums.lvl_stage import LvlStage
from game_level import GameLevel
from state_setback_command import StateSetbackCommand
import utils


# fixme completness should be taken only once player enters achievement window NOW it is taken on every frame


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode((game_constants.SCREEN_WIDTH, game_constants.SCREEN_HEIGHT))
        self._state = GameState.GAME_MODE_CHOOSING
        self._navigator = Navigator()
        self._achievement_manager = AchievementManager(game_constants.ACHIEVEMENTS_INFO_PATH)
        self._currencies_manager = CurrenciesManager(game_constants.CURRENCIES_INFO_PATH)

        # -------------------------- BACKGROUNDS --------------------------
        self._menu_bg = game_constants.MENU_BACKGROUND
        self._achievements_bg = game_constants.ACHIEVEMENTS_BACKGROUND
        self._mode_choosing_bg = game_constants.MODE_SELECTION_BACKGROUND
        self._level_choosing_bg = game_constants.LVL_SHOOSING_BACKGROUND
        # -------------------------- BACKGROUNDS --------------------------

        # -------------------------- BUTTONS --------------------------
        self._menu_buttons = utils.init_buttons_from_info(game_constants.MENU_BUTTONS_INFO,
                                                          lambda info: SwitchStateCommand(self._navigator, info["state"]),
                                                          game_constants.MOUSE_KEY)
        self._game_choosing_buttons = utils.init_buttons_from_info(game_constants.MODE_SELECTION_BUTTONS_INFO,
                                                                   lambda info: SwitchStateCommand(self._navigator, info["state"]),
                                                                   game_constants.MOUSE_KEY)
        self._achievements_info = self._init_achievements_info()
        self._level_buttons = utils.init_buttons_from_info(game_constants.LVL_BUTTONS_INFO,
                                                           lambda info: SetLevelCommand(self._navigator, info["lvl_num"]),
                                                           game_constants.MOUSE_KEY)
        self._loser_options_buttons = self._init_loser_options_button()
        # -------------------------- BUTTONS --------------------------

        self._locked_level_icon = game_constants.LOCKED_LEVEL_IMAGE
        # keep track of escape button
        self._roll_back_button = KeyboardResponsive(pygame.K_ESCAPE)

        # levels
        self._levels = self._init_levels()

    def _draw_buttons(self, buttons, screen):
        for b in buttons:
            b.draw(screen)

    def _get_achievement_completness(self):
        # todo cache achievement completeness and get new only if needed
        res = self._achievement_manager.get_achievements_completeness()
        dummy = True
        if dummy:
            for key in res.keys():
                res[key] = True
        return res

    def _draw_achievement_buttons(self, screen):
        completeness_map = self._get_achievement_completness()
        for key in completeness_map.keys():
            # fixme delete later needed because not all images are ready
            if key not in self._achievements_info:
                continue
            if completeness_map[key]:
                self._achievements_info[key]["unlocked_button"].draw(screen)
            else:
                self._achievements_info[key]["locked_button"].draw(screen)

    def _display_achievement(self, screen, ach_name):
        completeness_map = self._get_achievement_completness()
        screen.blit(self._achievements_info[ach_name]["description"], game_constants.ACHIEVEMENT_DESCRIPTION_POS)
        if completeness_map[self._navigator.displayed_achievement]:
            screen.blit(self._achievements_info[ach_name]["unlocked_icon"], game_constants.ACHIEVEMENT_ICON_POS)
        else:
            screen.blit(self._achievements_info[ach_name]["locked_icon"], game_constants.ACHIEVEMENT_ICON_POS)

    def _process_achievements_buttons(self):
        completeness_map = self._get_achievement_completness()
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

    def _init_loser_options_button(self):
        loser_buttons_info = game_constants.LOSER_BUTTONS_INFO
        # bribe
        bribe_images = loser_buttons_info["bribe"]["images"]
        bribe_pos = loser_buttons_info["bribe"]["position"]
        idle_bribe, closed_bribe, opened_bribe = bribe_images
        open_bribe_button = Button(idle_bribe, opened_bribe, bribe_pos, game_constants.MOUSE_KEY,
                                   BribeCommand(self._navigator, self._currencies_manager, game_constants.BRIBE_COST))
        closed_bribe_button = Button(idle_bribe, closed_bribe, bribe_pos, game_constants.MOUSE_KEY,
                                   SwitchPlayStateCommand(self._navigator, LvlStage.LOSER_OPTIONS))

        # trial
        trial_images = loser_buttons_info["trial"]["images"]
        trial_pos = loser_buttons_info["trial"]["position"]
        idle_trial, closed_trial, opened_trial = trial_images
        open_trial_button = Button(idle_trial, opened_trial, trial_pos, game_constants.MOUSE_KEY,
                                   TrialCommand(self._navigator, self._currencies_manager,
                                                game_constants.TRIAL_OF_THE_SEVEN_COST))
        closed_trial_button = Button(idle_trial, closed_trial, trial_pos, game_constants.MOUSE_KEY,
                                     SwitchPlayStateCommand(self._navigator, LvlStage.LOSER_OPTIONS))

        # back to level panel
        back_to_levels_images = loser_buttons_info["menu"]["images"]
        idle_levels, addressing_levels = back_to_levels_images
        levels_pos = loser_buttons_info["menu"]["position"]
        back_to_levels_button = Button(idle_levels, addressing_levels, levels_pos, game_constants.MOUSE_KEY,
                                       StateSetbackCommand(self._navigator))
        loser_buttons = {"bribe": {"opened": open_bribe_button, "closed": closed_bribe_button},
                         "trial": {"opened": open_trial_button, "closed": closed_trial_button},
                         "menu": back_to_levels_button}
        return loser_buttons

    def _init_achievements_info(self):
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

    def _draw_level_buttons(self, screen):
        levels_availability = self._get_levels_availability()
        for button, is_available in zip(self._level_buttons, levels_availability):
            if is_available:
                button.draw(screen)
            else:
                pos = button.draw_position
                screen.blit(self._locked_level_icon, pos)

    def _process_level_buttons(self):
        levels_availability = self._get_levels_availability()
        for level_index, (button, is_available) in enumerate(zip(self._level_buttons, levels_availability)):
            if is_available:
                user_intention = button.get_user_intention_and_update_track()
                if user_intention == UserIntention.SWITCH_OFF:
                    self._levels[level_index].activate_events()
                    self._levels[level_index].nullify_progress()
                    button.click()

    def _init_levels(self):
        levels = []
        configs_paths = [os.path.join(game_constants.LEVELS_CONFIGS_PATH, p)
                         for p in sorted(os.listdir(game_constants.LEVELS_CONFIGS_PATH))]
        persistent_info_paths = [os.path.join(game_constants.PERSISTENT_LEVEL_INFO_PATH, p)
                                 for p in sorted(os.listdir(game_constants.PERSISTENT_LEVEL_INFO_PATH))]
        for cfg_path, persistent_cfg_path in zip(configs_paths, persistent_info_paths):
            level = GameLevel(game_constants.MOUSE_KEY, persistent_cfg_path, cfg_path, self._navigator,
                              self._currencies_manager, self._achievement_manager,
                              self._loser_options_buttons, None)  # todo init winner options
            levels.append(level)
        return levels

    # fixme levels dont have configs for now so dummy version is used for now
    def _get_levels_availability(self):
        dummy = [False] * 100
        dummy[0] = True
        return dummy

    def update(self):
        # detect escape command
        go_back = self._roll_back_button.get_user_intention_and_update_track() == UserIntention.SWITCH_OFF
        if go_back:
            self._navigator.go_back()
        # update corresponding to current state
        if self._navigator.current_state == GameState.MENU:
            utils.process_buttons(self._menu_buttons)
        if self._navigator.current_state == GameState.GAME_MODE_CHOOSING:
            utils.process_buttons(self._game_choosing_buttons)
        if self._navigator.current_state == GameState.LEVEL_CHOOSING:
            self._process_level_buttons()
        if self._navigator.current_state == GameState.ACHIEVEMENTS:
            self._process_achievements_buttons()
        if self._navigator.current_state == GameState.PLAY:
            self._levels[self._navigator.played_level - 1].update()
        if self._navigator.current_state == GameState.EXIT:
            sys.exit()

    def draw(self, screen):
        if self._navigator.current_state == GameState.MENU:
            screen.blit(self._menu_bg, (0, 0))
            self._draw_buttons(self._menu_buttons, screen)
        if self._navigator.current_state == GameState.GAME_MODE_CHOOSING:
            screen.blit(self._mode_choosing_bg, (0, 0))
            self._draw_buttons(self._game_choosing_buttons, screen)
        if self._navigator.current_state == GameState.ACHIEVEMENTS:
            screen.blit(self._achievements_bg, (0, 0))
            self._draw_achievement_buttons(screen)
        if self._navigator.current_state == GameState.ACHIEVEMENT_VIEW:
            screen.blit(self._achievements_bg, (0, 0))
            ach_name = self._navigator.displayed_achievement
            self._display_achievement(screen, ach_name)
        if self._navigator.current_state == GameState.LEVEL_CHOOSING:
            screen.blit(self._level_choosing_bg, (0, 0))
            self._draw_level_buttons(screen)
        if self._navigator.current_state == GameState.PLAY:
            self._levels[self._navigator.played_level - 1].draw(screen)

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
