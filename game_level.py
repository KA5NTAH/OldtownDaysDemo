from responsive_objects.slide import Slide
from responsive_objects.mouse_responsive import MouseResponsive
from link import Link
import os
from droplet import Droplet  # fixme is it necessary
from channel import Channel
import game_constants
from game_enums.bonuses import Bonuses
from game_enums.lvl_stage import LvlStage
from game_enums.coins_kinds import CoinsKinds
from game_enums.user_intention import UserIntention
from challenge import Challenge
from game_enums.metals import Metals
from game_enums.achievement_tracking_values import AchievementTrackingValues
from game_enums.link_stage import LinkStage
from coin import Coin
import pygame
import numpy as np
import random as rd
import utils
from collections import deque
import sys
from typing import List
from persistent_objects.persistent_object import PersistentObject
import json
import utils
from switch_play_state_command import SwitchPlayStateCommand
from navigator import Navigator
from achievement_manager import AchievementManager
from persistent_objects.currencies_manager import CurrenciesManager
from game_enums.game_state import GameState


# todo implement bonus
# todo finish draw functions: draw fail/winning progress
# todo add winner and loser options
# todo add trial of the seven
# todo add buttons for winner/loser options + backgrounds
# todo add new command ------ DONE
# todo add play state support in navigator and level should interact with state through navigator --- DOING
# fixme maybe currencies manager and achievement manager should be attibutes of the game level PROBABLY
# todo add images for buttons
# todo add images for progress
# todo add bonus interaction and images for bonus
# todo init buttons like this
# def __init__(self, idle_image, addressing_image, position, mouse_button, command: Command):


class GameLevel(MouseResponsive, Slide, PersistentObject):
    def __init__(self, mouse_key: int, persistent_cfg_path: str, level_info_cfg_path: str, navigator: Navigator,
                 currencies_manager: CurrenciesManager, achievement_manager: AchievementManager,
                 loser_options_buttons, winner_options_buttons):
        super().__init__(mouse_key)
        PersistentObject.__init__(self, persistent_cfg_path)
        self._level_parameters_cfg_path = level_info_cfg_path
        self._availability_info = {"unlocked": False}
        self._init_from_file()
        self._navigator = navigator

        self._winner_options_buttons = winner_options_buttons
        self._currencies_manager = currencies_manager
        self._achievement_manager = achievement_manager
        # CONFIG PARAMETERS
        self._metals = None
        self._channels = None
        self._coins_frequency = None
        self._metal_challenge_dict = None
        self._current_challenge = None
        self._controlled_link = None
        self._drops_frequency = None
        self._coins_prob_distribution = None
        self._fails_limit = None
        self._droplets_queue = None
        # CONFIG PARAMETERS
        self._init_from_config()

        # set progress to zero
        self._robbed_channel_index = None
        self._fails_count = 0
        self._links_count = len(self._metals)
        self._complete_links_dict = dict.fromkeys(self._metals, False)
        self._complete_links_count = 0
        self._coins = []
        # ------------------ BACKGROUNDS --------------
        self._level_background = game_constants.LVL_BACKGROUND
        self._loser_options_background = game_constants.LOSER_OPTIONS_BACKGROUND
        # ------------------ BACKGROUNDS --------------

        # ------------------ BUTTONS PARAMETERS ------------------
        # WINNER OPTIONS
        # LOSER OPTIONS
        self._loser_options_buttons = loser_options_buttons
        # undefined yet trial and bribe buttons
        self._current_trial_button = None
        self._current_bribe_button = None
        # WINNER OPTIONS

        self.nullify_progress()
        self._relative_movement = pygame.mouse.get_rel()

    def nullify_progress(self):
        # channel from which player get controlled link
        self._robbed_channel_index = None
        self._fails_count = 0
        self._links_count = len(self._metals)
        self._complete_links_dict = dict.fromkeys(self._metals, False)
        self._complete_links_count = 0
        # init channels again
        self._init_channels()
        self._init_droplets_deque()
        self._coins = []

    def _set_looser_buttons(self):
        # set bribe button
        if self._currencies_manager.targ_coins_balance >= game_constants.BRIBE_COST:
            self._current_bribe_button = self._loser_options_buttons["bribe"]["opened"]
        else:
            self._current_bribe_button = self._loser_options_buttons["bribe"]["closed"]

        # set trial button
        if self._currencies_manager.faith_coins_balance >= game_constants.TRIAL_OF_THE_SEVEN_COST:
            self._current_trial_button = self._loser_options_buttons["trial"]["opened"]
        else:
            self._current_trial_button = self._loser_options_buttons["trial"]["closed"]

    def _init_droplets_deque(self):
        with open(self._level_parameters_cfg_path) as file:
            level_parameters = json.load(file)
            deque_data = self._metals * level_parameters["Droplets_per_metal_amount"]
            rd.shuffle(deque_data)
            self._droplets_queue = deque(deque_data)

    def _init_from_config(self):
        with open(self._level_parameters_cfg_path) as file:
            level_parameters = json.load(file)
            self._fails_limit = level_parameters["Fails_limit"]
            self._coins_prob_distribution = level_parameters["Coins_probability"]
            self._drops_frequency = level_parameters["Drops_frequency"]
            self._coins_frequency = level_parameters["Coins_frequency"]
            metals = [Metals._member_map_[cfg_str] for cfg_str in level_parameters["Links"]]
            self._metals = metals
            self._init_droplets_deque()
            self._init_channels()
            # init challenges
            self._metal_challenge_dict = {}
            challenges_time = level_parameters["Challenges_time"]
            for metal in metals:
                challenge_info = level_parameters["Challenges"][metal.name]
                coordinates = np.array(challenge_info["coordinates"])
                timer_color = challenge_info["timer_color"]
                # fixme now only gold because not all images are ready yet
                challenge = Challenge(coordinates, Metals.GOLD, challenges_time, timer_color, game_constants.MOUSE_KEY)
                self._metal_challenge_dict[metal] = challenge

    def _init_from_file(self):
        print("init from file")
        if not os.path.exists(self._config_path):
            print("dump into file ")
            self.dump_into_file()
        else:
            with open(self._config_path) as file:
                self._availability_info = json.load(file)

    def _init_channels(self):
        """initialize channels with links. Info about links is drawn from metals list and game constant.
        game constants provide images for links of every metal and their positional arrangement based on their numbers
        """
        channels = []
        with open(self._level_parameters_cfg_path) as file:
            level_parameters = json.load(file)
            filling_rate = level_parameters["Link_filling_rate"]
            time = level_parameters["Challenge_wait_time"]
            links_coordinates = game_constants.LINKS_COORDINATES[len(self._metals)]
            for metal, coord in zip(self._metals, links_coordinates):
                images = game_constants.LINKS_IMAGES[metal]
                link = Link(*images, filling_rate, coord, time, metal, game_constants.MOUSE_KEY)
                channels.append(Channel(link))
        self._channels = channels

    def dump_into_file(self):
        with open(self._config_path, 'w') as file:
            json.dump(self._availability_info, file)

    def activate_events(self):
        pygame.time.set_timer(game_constants.GENERATE_DROP_EVENT.type, self._drops_frequency)
        pygame.time.set_timer(game_constants.GENERATE_COIN_EVENT.type, self._coins_frequency)

    def deactivate_events(self):
        pygame.time.set_timer(game_constants.GENERATE_DROP_EVENT.type, 0)
        pygame.time.set_timer(game_constants.GENERATE_COIN_EVENT.type, 0)

    def _handle_events(self):
        for event in pygame.event.get(game_constants.LVL_EVENTS_TYPES):
            if self._navigator.current_level_state == LvlStage.USUAL_PLAY:
                if event.type == game_constants.GENERATE_COIN_EVENT.type:
                    self._generate_coin()
                elif event.type == game_constants.GENERATE_DROP_EVENT.type:
                    self._set_drop_at_random_channel()
                elif event.type == game_constants.RUINED_DROP_EVENT.type:
                    self._fails_count += 1
                    if self._fails_count == self._fails_limit:
                        self._controlled_link = None
                        self._robbed_channel_index = None
                        self._set_looser_buttons()
                        self._navigator.switch_to_play_state(LvlStage.LOSER_OPTIONS)
                elif event.type in game_constants.EVENT_TYPE_NO_LINK_RUIN_METAL_DICT:
                    metal = game_constants.EVENT_TYPE_NO_LINK_RUIN_METAL_DICT[event.type]
                    if not self._complete_links_dict[metal]:
                        self._fails_count += 1
                elif event.type in game_constants.LINK_IS_DONE_EVENTS_TYPES:
                    self._complete_links_count += 1
                    print(f'COMPLETED : {self._complete_links_count}')
                    metal = game_constants.EVENT_TYPE_METAL_DICT[event.type]
                    self._complete_links_dict[metal] = True

    def _refresh_expiring_objects(self):
        """
        Update clock of expiring objects in order to not substract some period of time from their life time
        For example when player returns to usual play after challenge, time that he has spent in challenge
        should not be counted as passed lifetime of coins
        """
        for coin_ind in range(len(self._coins)):
            self._coins[coin_ind].refresh_clock()
        for channel_ind in range(len(self._channels)):
            if self._channels[channel_ind].link_is_available():
                self._channels[channel_ind].refresh_link()

    def _handle_user_link_actions(self, achievement_manager, currencies_manager):
        # if there is no link Player might get one under control
        if self._controlled_link is None:
            for channel_num in range(len(self._channels)):
                if not self._channels[channel_num].link_is_available():
                    continue
                # all links intentions must be updated during this loop
                link_intention = self._channels[channel_num].get_and_update_link_intention()
                if link_intention == UserIntention.SWITCH_ON:
                    if self._channels[channel_num].link_stage == LinkStage.CHALLENGE_PROPOSAL:
                        metal = self._channels[channel_num].link_metal
                        print(f'CHALLENGE : {metal}')
                        self._current_challenge = self._metal_challenge_dict[metal]
                        self._current_challenge.refresh_clock()
                        self._navigator.switch_to_play_state(LvlStage.CHALLENGE)
                    else:
                        self._controlled_link = self._channels[channel_num].yield_link()
                        self._robbed_channel_index = channel_num
        else:
            """
            If link is controlled then player is either:
            1) keeps moving link
            2) releases link
            """
            ctrl_link_intention = self._controlled_link.get_user_intention_and_update_track()
            if ctrl_link_intention == UserIntention.KEEP_ON_STATE:
                self._controlled_link.move(self._relative_movement)
            elif ctrl_link_intention == UserIntention.SWITCH_OFF:
                """
                When link is released there are two strategies:
                1) Link is released in such place that it has iou with other link > threshold: In such case links are 
                swapped
                2) Otherwise link is returned back
                """
                for channel_num in range(len(self._channels)):
                    if channel_num == self._robbed_channel_index:
                        continue
                    iou = utils.get_iou(self._channels[channel_num].link_rect, self._controlled_link.addressing_rect)
                    if iou >= game_constants.LINKS_SWAP_THRD:
                        swap_link = self._channels[channel_num].yield_link()
                        self._channels[channel_num].set_link(self._controlled_link)
                        self._channels[self._robbed_channel_index].set_link(swap_link)
                        # link is controlled no more
                        self._controlled_link = None
                        self._robbed_channel_index = None
                        break
                else:
                    # return link back if there is no one to swap with
                    self._channels[self._robbed_channel_index].set_link(self._controlled_link)
                    self._controlled_link = None
                    self._robbed_channel_index = None

    def _handle_user_coin_actions(self, achievement_manager, currencies_manager):
        """
        register user's actions directed at coins
        if coin is picked method tells about it to currencies_manager and achievement_manager
        picked coins are discarded
        """
        indexes_to_keep = []
        for coin_index in range(len(self._coins)):
            coin_intention = self._coins[coin_index].get_user_intention_and_update_track()
            if coin_intention == UserIntention.SWITCH_ON:
                kind = self._coins[coin_index].coin_kind
                if kind == CoinsKinds.BLACKFYRE_COIN:
                    achievement_manager.update_tracking_value(AchievementTrackingValues.COLLECTED_BLACKFYRE_COINS)
                else:
                    currencies_manager.record_coin_pick(kind)
                    if kind == CoinsKinds.TARGARYEN_COIN:
                        achievement_manager.update_tracking_value(AchievementTrackingValues.COLLECTED_GOLD)
                    if kind == CoinsKinds.FAITH_COIN:
                        achievement_manager.update_tracking_value(AchievementTrackingValues.COLLECTED_FAITH_COINS)
            else:
                indexes_to_keep.append(coin_index)
        self._coins = [c for (ind, c) in enumerate(self._coins) if ind in indexes_to_keep]

    def _handle_successful_challenge(self):
        # todo implement
        pass

    def update(self):
        """Level update"""
        self._relative_movement = pygame.mouse.get_rel()  # update relative movement lvl
        self._handle_events()
        if self._navigator.current_level_state == LvlStage.USUAL_PLAY:
            if self._fails_count == self._fails_limit:
                self._set_looser_buttons()  # todo where to put?
                self._navigator.switch_to_play_state(LvlStage.LOSER_OPTIONS)  # fixme put in the same method??
            if self._complete_links_count == self._links_count:
                self._navigator.switch_to_state(GameState.LEVEL_WINNER_OPTIONS)
            self._handle_user_link_actions(self._achievement_manager, self._currencies_manager)
            self._handle_user_coin_actions(self._achievement_manager, self._currencies_manager)
            for coin_index in range(len(self._coins)):
                self._coins[coin_index].update_ttl()
            for chan_index in range(len(self._channels)):
                self._channels[chan_index].update()
        elif self._navigator.current_level_state == LvlStage.CHALLENGE:
            success = self._current_challenge.update_and_return_result(self._achievement_manager)
            if success is not None:
                if success:
                    self._handle_successful_challenge()
                print(f'BACK TO LEVEL with {success}')
                self._refresh_expiring_objects()
                self._navigator.switch_to_play_state(LvlStage.USUAL_PLAY)
        elif self._navigator.current_level_state == LvlStage.LOSER_OPTIONS:
            utils.process_buttons([self._current_bribe_button,
                                   self._current_trial_button,
                                   self._loser_options_buttons["menu"]])
        elif self._navigator.current_level_state == LvlStage.TRIAL_OF_THE_SEVEN:
            pass

        # discard expired coins
        # self._coins = [c for c in self._coins if c.is_still_alive()]

    def draw(self, screen):
        if self._navigator.current_level_state == LvlStage.USUAL_PLAY:
            screen.blit(self._level_background, (0, 0))
            for coin in self._coins:
                coin.draw(screen)
            for channel in self._channels:
                channel.draw(screen)
            if self._controlled_link is not None:
                self._controlled_link.draw(screen)
        elif self._navigator.current_level_state == LvlStage.CHALLENGE:
            self._current_challenge.draw(screen)
        elif self._navigator.current_level_state == LvlStage.LOSER_OPTIONS:
            screen.blit(self._loser_options_background, (0, 0))
            self._current_trial_button.draw(screen)
            self._current_bribe_button.draw(screen)
            self._loser_options_buttons["menu"].draw(screen)

    def _generate_coin(self):
        """generates coins based on probability distribution = [p1, p2, p3] where:
         p1 - probability of targaryen coin
         p2 - probability of faith coin
         p3 - probability of blackfyre coin
        """
        coin_kind = np.random.choice([CoinsKinds.TARGARYEN_COIN,
                                      CoinsKinds.FAITH_COIN,
                                      CoinsKinds.BLACKFYRE_COIN], p=self._coins_prob_distribution)
        x_position = rd.randrange(*game_constants.COINS_X_BOUNDARIES)
        y_position = rd.randrange(*game_constants.COINS_Y_BOUNDARIES)
        coin = Coin(coin_kind, x_position, y_position, game_constants.MOUSE_KEY, 3.5 * 1000)
        self._coins.append(coin)

    def _set_drop_at_random_channel(self):
        index = rd.randrange(len(self._channels))
        metal = self._droplets_queue.pop()
        self._channels[index].create_and_set_ball(metal)


if __name__ == "__main__":
    test_level = True
    if test_level:
        pygame.init()
        persistent_info = "E:\\develop\\OldtownDays\\persistent_info\\levels_info\\001.json"
        level_parameters = "E:\\develop\\OldtownDays\\levels_parameters\\001.json"
        navigator = Navigator()
        from game_enums.game_state import GameState
        navigator.switch_to_state(GameState.PLAY)
        Lvl = GameLevel(game_constants.MOUSE_KEY, persistent_info, level_parameters, navigator)
        Lvl.activate_events()
        screen = pygame.display.set_mode((1200, 680))
        am = AchievementManager("am.json")
        cm = CurrenciesManager("cm.json")
        while True:
            events = pygame.event.get((pygame.QUIT, ))
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.fill((255, 255, 255))
            # update block
            Lvl.update()
            # draw block
            Lvl.draw(screen)
            pygame.display.flip()


