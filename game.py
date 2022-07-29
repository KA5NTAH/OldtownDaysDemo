from enum import Enum, auto
import pygame
from game_enums.game_state import GameState
from game_enums.bonuses import Bonuses
from game_enums.achievement_tracking_values import AchievementTrackingValues
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
from next_level_command import NextLevelCommand
from winner_back_to_level_command import WinnerBackToLevelCommand
from education_forward_command import EducationalForwardCommand
from education_back_command import EducationBackCommand
from responsive_objects.keyboard_button import KeyboardButton
from game_enums.metals import Metals
from challenge import Challenge
import utils


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode(
            (game_constants.SCREEN_WIDTH, game_constants.SCREEN_HEIGHT)
        )
        self._state = GameState.GAME_MODE_CHOOSING
        self._navigator = Navigator()
        self._achievement_manager = AchievementManager(
            game_constants.ACHIEVEMENTS_INFO_PATH
        )
        self._currencies_manager = CurrenciesManager(
            game_constants.CURRENCIES_INFO_PATH
        )
        self.stranger_challenge = Challenge(
            game_constants.STRANGER_CHALLENGE_COORDIANTES,
            Metals.BLACK_IRON,
            game_constants.STRANGER_CHALLENGE_TIME,
            game_constants.MOUSE_KEY,
            game_constants.STRANGER_CHALLENGE_BG,
        )

        # -------------------------- BACKGROUNDS --------------------------
        self._menu_bg = game_constants.MENU_BACKGROUND
        self._achievements_bg = game_constants.ACHIEVEMENTS_BACKGROUND
        self._mode_choosing_bg = game_constants.MODE_SELECTION_BACKGROUND
        self._level_choosing_bg = game_constants.LVL_SHOOSING_BACKGROUND
        # -------------------------- BACKGROUNDS --------------------------

        # -------------------------- BUTTONS --------------------------
        self._menu_buttons = utils.init_buttons_from_info(
            game_constants.MENU_BUTTONS_INFO,
            lambda info: SwitchStateCommand(self._navigator, info["state"]),
            game_constants.MOUSE_KEY,
        )
        self._game_choosing_buttons = utils.init_buttons_from_info(
            game_constants.MODE_SELECTION_BUTTONS_INFO,
            lambda info: SwitchStateCommand(self._navigator, info["state"]),
            game_constants.MOUSE_KEY,
        )
        self._achievements_info = self._init_achievements_info()
        self._level_buttons = utils.init_buttons_from_info(
            game_constants.LVL_BUTTONS_INFO,
            lambda info: SetLevelCommand(self._navigator, info["lvl_num"]),
            game_constants.MOUSE_KEY,
        )
        self._loser_options_buttons = self._init_loser_options_button()
        self._winner_options_buttons = (
            self._init_winner_options_buttons()
        )  # next_lvl_button, back_to_levels_button
        # -------------------------- BUTTONS --------------------------

        self._locked_level_icon = game_constants.LOCKED_LEVEL_IMAGE
        # keep track of escape button
        self._roll_back_button = KeyboardResponsive(pygame.K_ESCAPE)

        # levels
        self._levels = self._init_levels()
        self._levels[0].unlock()
        self._level_number = len(self._levels)
        self.education_forward = KeyboardButton(
            pygame.K_RIGHT, EducationalForwardCommand(self._navigator)
        )
        self.education_back = KeyboardButton(
            pygame.K_LEFT, EducationBackCommand(self._navigator)
        )

        self.infinite_level = GameLevel(
            game_constants.MOUSE_KEY,
            game_constants.INFINITE_LVL_PERS_CFG,
            game_constants.INFINITE_LVL_CFG,
            self._navigator,
            self._currencies_manager,
            self._achievement_manager,
            self._loser_options_buttons,
            self.stranger_challenge,
            mode="infinite",
        )

    def _draw_buttons(self, buttons, screen):
        for b in buttons:
            b.draw(screen)

    def _get_achievement_completness(self):
        res = self._achievement_manager.get_achievements_completeness()
        return res

    def _draw_achievement_buttons(self, screen):
        completeness_map = self._get_achievement_completness()
        for key in completeness_map.keys():
            if key not in self._achievements_info:
                continue
            if completeness_map[key]:
                self._achievements_info[key]["unlocked_button"].draw(screen)
            else:
                self._achievements_info[key]["locked_button"].draw(screen)

    def _display_achievement(self, screen, ach_name):
        completeness_map = self._get_achievement_completness()
        screen.blit(
            self._achievements_info[ach_name]["description"],
            game_constants.ACHIEVEMENT_DESCRIPTION_POS,
        )
        if completeness_map[self._navigator.displayed_achievement]:
            screen.blit(
                self._achievements_info[ach_name]["unlocked_icon"],
                game_constants.ACHIEVEMENT_ICON_POS,
            )
        else:
            screen.blit(
                self._achievements_info[ach_name]["locked_icon"],
                game_constants.ACHIEVEMENT_ICON_POS,
            )

    def _process_achievements_buttons(self):
        completeness_map = self._get_achievement_completness()
        for key in completeness_map.keys():
            # fixme delete later needed because not all images are ready
            if key not in self._achievements_info:
                continue
            if completeness_map[key]:
                user_intention = self._achievements_info[key][
                    "unlocked_button"
                ].get_user_intention_and_update_track()
                if user_intention == UserIntention.SWITCH_OFF:
                    self._achievements_info[key]["unlocked_button"].click()
            else:
                user_intention = self._achievements_info[key][
                    "locked_button"
                ].get_user_intention_and_update_track()
                if user_intention == UserIntention.SWITCH_OFF:
                    self._achievements_info[key]["locked_button"].click()

    def _init_loser_options_button(self):
        loser_buttons_info = game_constants.LOSER_BUTTONS_INFO
        # bribe
        bribe_images = loser_buttons_info["bribe"]["images"]
        bribe_pos = loser_buttons_info["bribe"]["position"]
        idle_bribe, closed_bribe, opened_bribe = bribe_images
        open_bribe_button = Button(
            idle_bribe,
            opened_bribe,
            bribe_pos,
            game_constants.MOUSE_KEY,
            BribeCommand(
                self._navigator, self._currencies_manager, game_constants.BRIBE_COST
            ),
        )
        closed_bribe_button = Button(
            idle_bribe,
            closed_bribe,
            bribe_pos,
            game_constants.MOUSE_KEY,
            SwitchPlayStateCommand(self._navigator, LvlStage.LOSER_OPTIONS),
        )

        # trial
        trial_images = loser_buttons_info["trial"]["images"]
        trial_pos = loser_buttons_info["trial"]["position"]
        idle_trial, closed_trial, opened_trial = trial_images
        open_trial_button = Button(
            idle_trial,
            opened_trial,
            trial_pos,
            game_constants.MOUSE_KEY,
            TrialCommand(
                self._navigator,
                self._currencies_manager,
                game_constants.TRIAL_OF_THE_SEVEN_COST,
            ),
        )
        closed_trial_button = Button(
            idle_trial,
            closed_trial,
            trial_pos,
            game_constants.MOUSE_KEY,
            SwitchPlayStateCommand(self._navigator, LvlStage.LOSER_OPTIONS),
        )

        # back to level panel
        back_to_levels_images = loser_buttons_info["menu"]["images"]
        idle_levels, addressing_levels = back_to_levels_images
        levels_pos = loser_buttons_info["menu"]["position"]
        back_to_levels_button = Button(
            idle_levels,
            addressing_levels,
            levels_pos,
            game_constants.MOUSE_KEY,
            StateSetbackCommand(self._navigator),
        )
        loser_buttons = {
            "bribe": {"opened": open_bribe_button, "closed": closed_bribe_button},
            "trial": {"opened": open_trial_button, "closed": closed_trial_button},
            "menu": back_to_levels_button,
        }
        return loser_buttons

    def _init_winner_options_buttons(self):
        next_lvl_button = Button(
            *game_constants.WINNER_OPTIONS_INFO["next_level"]["images"],
            game_constants.WINNER_OPTIONS_INFO["next_level"]["position"],
            game_constants.MOUSE_KEY,
            NextLevelCommand(self._navigator)
        )

        back_to_levels_button = Button(
            *game_constants.WINNER_OPTIONS_INFO["back_to_menu"]["images"],
            game_constants.WINNER_OPTIONS_INFO["back_to_menu"]["position"],
            game_constants.MOUSE_KEY,
            WinnerBackToLevelCommand(self._navigator)
        )
        return [next_lvl_button, back_to_levels_button]

    def _init_achievements_info(self):
        achievements_info = {}
        for key, pos in zip(
            game_constants.ACHIEVEMENTS_IMAGES.keys(),
            game_constants.ACHIEVEMENT_POSITIONS,
        ):
            (
                small_icon_locked,
                small_icon_unlocked,
                big_icon_locked,
                big_icon_unlocked,
                description,
            ) = game_constants.ACHIEVEMENTS_IMAGES[key]
            command = SetAchievementCommand(self._navigator, key)
            locked_button = Button(
                small_icon_locked,
                small_icon_locked,
                pos,
                game_constants.MOUSE_KEY,
                command,
            )
            unlocked_button = Button(
                small_icon_unlocked,
                small_icon_unlocked,
                pos,
                game_constants.MOUSE_KEY,
                command,
            )
            achievement_info = {
                "locked_button": locked_button,
                "unlocked_button": unlocked_button,
                "locked_icon": big_icon_locked,
                "unlocked_icon": big_icon_unlocked,
                "description": description,
            }
            achievements_info[key] = achievement_info
        return achievements_info

    def _draw_level_buttons(self, screen):
        levels_availability = self._get_levels_availability()
        # fixme now there is more buttons than there is levels
        for button, is_available in zip(
            self._level_buttons[: self._level_number],
            levels_availability[: self._level_number],
        ):
            if is_available:
                button.draw(screen)
            else:
                pos = button.draw_position
                screen.blit(self._locked_level_icon, pos)

    def _process_level_buttons(self):
        levels_availability = self._get_levels_availability()
        for level_index, (button, is_available) in enumerate(
            zip(self._level_buttons, levels_availability)
        ):
            if is_available:
                user_intention = button.get_user_intention_and_update_track()
                if user_intention == UserIntention.SWITCH_OFF:
                    self._levels[level_index].activate_events()
                    self._levels[level_index].nullify_progress()
                    button.click()

    def _init_levels(self):
        levels = []
        configs_paths = [
            os.path.join(game_constants.LEVELS_CONFIGS_PATH, p)
            for p in sorted(os.listdir(game_constants.LEVELS_CONFIGS_PATH))
        ]
        persistent_info_paths = [
            os.path.join(game_constants.PERSISTENT_LEVEL_INFO_PATH, p)
            for p in sorted(os.listdir(game_constants.PERSISTENT_LEVEL_INFO_PATH))
        ]
        for cfg_path, persistent_cfg_path in zip(configs_paths, persistent_info_paths):
            level = GameLevel(
                game_constants.MOUSE_KEY,
                persistent_cfg_path,
                cfg_path,
                self._navigator,
                self._currencies_manager,
                self._achievement_manager,
                self._loser_options_buttons,
                self.stranger_challenge,
            )
            levels.append(level)
        return levels

    def _get_levels_availability(self):
        availability = []
        for level in self._levels:
            availability.append(level.is_available())
        return availability

    def update(self):
        # detect escape command
        go_back = (
            self._roll_back_button.get_user_intention_and_update_track()
            == UserIntention.SWITCH_OFF
        )
        if go_back:
            """if we return back from the game Current level events must be deactivated"""
            if self._navigator.current_state == GameState.PLAY:
                self._levels[self._navigator.played_level - 1].deactivate_events()
            if self._navigator.current_state == GameState.EDUCATION:
                self._navigator.current_education_step = 0
            self._navigator.go_back()
        # update corresponding to current state
        if self._navigator.current_state == GameState.MENU:
            utils.process_buttons(self._menu_buttons)
        if self._navigator.current_state == GameState.EDUCATION:
            utils.process_buttons([self.education_forward, self.education_back])
        if self._navigator.current_state == GameState.GAME_MODE_CHOOSING:
            utils.process_buttons(self._game_choosing_buttons)
            # if we clicked on infinte play then prepare level
            if self._navigator.current_state == GameState.INFINITE_PLAY:
                self.infinite_level.activate_events()
                self.infinite_level.nullify_progress()
        if self._navigator.current_state == GameState.INFINITE_PLAY:
            self.infinite_level.update()
        if self._navigator.current_state == GameState.LEVEL_CHOOSING:
            self._process_level_buttons()
        if self._navigator.current_state == GameState.ACHIEVEMENTS:
            self._process_achievements_buttons()
        if self._navigator.current_state == GameState.PLAY:
            self._levels[self._navigator.played_level - 1].update()
        if self._navigator.current_state == GameState.LEVEL_WINNER_OPTIONS:
            next_level_num = self._navigator.played_level + 1
            if next_level_num < self._level_number:
                self._levels[next_level_num - 1].unlock()
            if self._navigator.played_level == self._level_number:
                utils.process_buttons(
                    [self._winner_options_buttons[1]]
                )  # no next level allow only return to menu
            else:
                utils.process_buttons(self._winner_options_buttons)

        # check negative balance
        if (
            self._currencies_manager.targ_coins_balance < 0
            or self._currencies_manager.faith_coins_balance < 0
        ):
            self._achievement_manager.update_tracking_value(
                AchievementTrackingValues.NEGATIVE_BALANCE
            )

        if self._navigator.current_state == GameState.EXIT:
            self._currencies_manager.dump_into_file()
            self._achievement_manager.dump_into_file()
            for level in self._levels:
                level.dump_into_file()
            sys.exit()

    def draw(self, screen):
        if self._navigator.current_state == GameState.MENU:
            screen.blit(self._menu_bg, (0, 0))
            self._draw_buttons(self._menu_buttons, screen)
        if self._navigator.current_state == GameState.EDUCATION:
            current_step = self._navigator.current_education_step
            screen.blit(game_constants.EDUCATION_IMAGES[current_step], (0, 0))
            for i, coord in enumerate(game_constants.EDUCATIONAL_PROGRESS_COORD):
                if i == current_step:
                    pygame.draw.circle(
                        screen,
                        game_constants.EDUCATION_ACTIVE_COLOR,
                        coord,
                        game_constants.EDUCATIONAL_PROGRESS_RAD,
                    )
                else:
                    pygame.draw.circle(
                        screen,
                        game_constants.EDUCATION_NON_ACTIVE_COLOR,
                        coord,
                        game_constants.EDUCATIONAL_PROGRESS_RAD,
                    )
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
            screen.blit(
                game_constants.BONUSES_ICONS_IMAGES[self._navigator.bonus],
                game_constants.BONUS_MENU_COORD,
            )
            self._currencies_manager.draw(screen)
            self._draw_level_buttons(screen)
        if self._navigator.current_state == GameState.PLAY:
            self._levels[self._navigator.played_level - 1].draw(screen)
        if self._navigator.current_state == GameState.LEVEL_WINNER_OPTIONS:
            screen.blit(game_constants.WINNER_OPTIONS_BACKGROUND, (0, 0))
            if self._navigator.played_level == self._level_number:
                # draw only Back to menu button
                self._winner_options_buttons[1].draw(screen)
            else:
                self._draw_buttons(self._winner_options_buttons, screen)
        if self._navigator.current_state == GameState.INFINITE_PLAY:
            self.infinite_level.draw(screen)

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
