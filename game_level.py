import game_constants
from responsive_objects.slide import Slide
from responsive_objects.mouse_responsive import MouseResponsive
from link import Link
from droplet import Droplet
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


# todo implement bonus
# todo finish draw functions: draw fail/winning progress
# todo add winner and loser options
# todo add trial of the seven
# todo add persistent inheritance
class GameLevel(MouseResponsive, Slide):
    def __init__(self, mouse_key: int, metals: List[Metals], challenges: List[Challenge],
                 droplets_queue: deque, fails_limit: int, challenge_wait_time: int, coins_frequency: int,
                 drops_frequency: int, coins_prob_distribution: List[float]):
        super().__init__(mouse_key)
        self._stage = LvlStage.USUAL_PLAY
        self._channels = self._init_channels(metals, challenge_wait_time)
        self._metal_challenge_dict = dict(zip(metals, challenges))
        self._current_challenge = None
        self._controlled_link = None
        # channel from which player get controlled link
        self._robbed_channel_index = None
        self._fails_limit = fails_limit
        self._fails_count = 0
        self._links_count = len(metals)
        self._complete_links_dict = dict.fromkeys(metals, False)
        self._complete_links_count = 0
        # deque that represents metal order of droplets
        self._droplets_queue = droplets_queue
        self._coins_frequency = coins_frequency
        self._drops_frequency = drops_frequency
        self._coins_prob_distribution = coins_prob_distribution
        self._coins = []
        self._relative_movement = pygame.mouse.get_rel()

    def set_events(self):
        print(self._drops_frequency)
        pygame.time.set_timer(game_constants.GENERATE_DROP_EVENT.type, self._drops_frequency)
        pygame.time.set_timer(game_constants.GENERATE_COIN_EVENT.type, self._coins_frequency)

    def _handle_events(self):
        for event in pygame.event.get(game_constants.LVL_EVENTS_TYPES):
            if self._stage == LvlStage.USUAL_PLAY:
                if event.type == game_constants.GENERATE_COIN_EVENT.type:
                    self._generate_coin()
                elif event.type == game_constants.GENERATE_DROP_EVENT.type:
                    self._set_drop_at_random_channel()
                elif event.type == game_constants.RUINED_DROP_EVENT.type:
                    self._fails_count += 1
                    print(self._fails_count)
                    if self._fails_count == self._fails_limit:
                        self._controlled_link = None
                        self._robbed_channel_index = None
                        self._stage = LvlStage.LOSER_OPTIONS
                elif event.type in game_constants.EVENT_TYPE_NO_LINK_RUIN_METAL_DICT:
                    metal = game_constants.EVENT_TYPE_NO_LINK_RUIN_METAL_DICT[event.type]
                    if not self._complete_links_dict[metal]:
                        self._fails_count += 1
                elif event.type in game_constants.LINK_IS_DONE_EVENTS_TYPES:
                    for c in self._channels:
                        print(c._link)
                    self._complete_links_count += 1
                    print(f'COMPLETED : {self._complete_links_count}')
                    metal = game_constants.EVENT_TYPE_METAL_DICT[event.type]
                    self._complete_links_dict[metal] = True

    def _refresh_expiring_objects(self):
        """
        Update clock of expiring objects in order to not substract some period of time from their life time
        For example when player returns to usual play after challenge time that he has spent in challenge
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
                        self._stage = LvlStage.CHALLENGE
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

    def update(self, achievement_manager, currencies_manager):
        # todo write proper doc string
        """Level update"""
        self._relative_movement = pygame.mouse.get_rel()  # update relative movement lvl
        self._handle_events()
        if self._stage == LvlStage.USUAL_PLAY:
            if self._fails_count == self._fails_limit:
                self._stage = LvlStage.LOSER_OPTIONS
            if self._complete_links_count == self._links_count:
                self._stage = LvlStage.WINNER_OPTIONS
            self._handle_user_link_actions(achievement_manager, currencies_manager)
            self._handle_user_coin_actions(achievement_manager, currencies_manager)
            for coin_index in range(len(self._coins)):
                self._coins[coin_index].update_ttl()
            for chan_index in range(len(self._channels)):
                self._channels[chan_index].update()
        elif self._stage == LvlStage.CHALLENGE:
            success = self._current_challenge.update_and_return_result(achievement_manager)
            if success is not None:
                if success:
                    self._handle_successful_challenge()
                print(f'BACK TO LEVEL with {success}')
                self._refresh_expiring_objects()
                self._stage = LvlStage.USUAL_PLAY
        elif self._stage == LvlStage.LOSER_OPTIONS:
            pass
        elif self._stage == LvlStage.WINNER_OPTIONS:
            pass
        elif self._stage == LvlStage.TRIAL_OF_THE_SEVEN:
            pass

        # discard expired coins
        # self._coins = [c for c in self._coins if c.is_still_alive()]

    def draw(self, screen):
        if self._stage == LvlStage.USUAL_PLAY:
            screen.blit(game_constants.LVL_BACKGROUND, (0, 0))
            for coin in self._coins:
                coin.draw(screen)
            for channel in self._channels:
                channel.draw(screen)
            if self._controlled_link is not None:
                self._controlled_link.draw(screen)
        elif self._stage == LvlStage.CHALLENGE:
            self._current_challenge.draw(screen)
        elif self._stage == LvlStage.LOSER_OPTIONS:
            screen.fill((255, 0, 0))
        elif self._stage == LvlStage.WINNER_OPTIONS:
            screen.fill((0, 255, 0))

    def _init_channels(self, metals, time):
        """initialize channels with links. Info about links is drawn from metals list and game constant.
        game constants provide images for links of every metal and their positional arrangement based on their numbers
        """
        links_coordinates = game_constants.LINKS_COORDINATES[len(metals)]
        channels = []
        for metal, coord in zip(metals, links_coordinates):
            images = game_constants.LINKS_IMAGES[metal]
            link = Link(*images, coord, time, metal, game_constants.MOUSE_KEY)
            channels.append(Channel(link))
        return channels

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
    pygame.init()
    links_metals = [Metals.GOLD,
                    Metals.BRONZE,
                    Metals.BLACK_IRON,
                    Metals.SILVER,
                    Metals.COPPER]
    droplets = deque(links_metals * 100)
    ccord = [[100, 100],
             [500, 200],
             [900, 100],
             [1000, 500],
             [100, 600]]
    c = Challenge(ccord, Metals.GOLD, 10000, (255, 0, 0), 0)
    c1 = Challenge(ccord, Metals.GOLD, 10000, (255, 0, 0), 0)
    c2 = Challenge(ccord, Metals.GOLD, 10000, (255, 0, 0), 0)
    c3 = Challenge(ccord, Metals.GOLD, 10000, (255, 0, 0), 0)
    c4 = Challenge(ccord, Metals.GOLD, 10000, (255, 0, 0), 0)
    challenges = [c, c1, c2, c3, c4]
    Lvl = GameLevel(game_constants.MOUSE_KEY, links_metals, challenges, droplets, 1000, 100, 3000, 100, [0.6, 0.3, 0.1])
    Lvl.set_events()
    screen = pygame.display.set_mode((1200, 680))

    from achievement_manager import AchievementManager
    from persistent_objects.currencies_manager import CurrenciesManager
    am = AchievementManager("am.json")
    cm = CurrenciesManager("cm.json")
    while True:
        events = pygame.event.get((pygame.QUIT, ))
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((255, 255, 255))
        # update block
        Lvl.update(am, cm)
        # draw block
        Lvl.draw(screen)
        pygame.display.flip()


