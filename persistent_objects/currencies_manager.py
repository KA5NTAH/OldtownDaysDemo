from persistent_objects.persistent_object import PersistentObject
from game_enums.coins_kinds import CoinsKinds
import game_constants
import pygame
import json
import os


class CurrenciesManager(PersistentObject):
    """Class is responsible for storing info about currencies throughout all game sessions"""
    def __init__(self, config_path):
        super().__init__(config_path)
        self._currencies_info = {CoinsKinds.TARGARYEN_COIN.name: 0,
                                 CoinsKinds.FAITH_COIN.name: 0}
        self._drawing_w = 257
        self._drawing_h = 158
        # todo import images in game_constants
        self._drawing_bg = game_constants.CURRENCIES_MANAGER_BG
        self._targ_coin_miniature = game_constants.TARG_COIN_MINIATURE
        self._faith_coin_miniauture = game_constants.FAITH_COIN_MINIATURE
        _, _, self._coin_w, self._coin_h = self._targ_coin_miniature.get_rect()
        self._coin_border_offset = (20, 10)
        self._coin_text_offset = (10, 10)
        self._coins_y_gap = 20
        self._font = pygame.font.SysFont(None, 48)
        self._text_color = (255, 255, 255)
        self._init_from_file()

    def draw(self, screen, position=None):
        """
        Draws info about collected coins.
        By defaults it is drawn in a right up corner, but position could be set
        """
        if position is None:
            position = (game_constants.SCREEN_WIDTH - self._drawing_w, 0)
        targ_coin_position = (position[0] + self._coin_border_offset[0],
                              position[1] + self._coin_border_offset[1])
        faith_coin_position = (position[0] + self._coin_border_offset[0],
                               position[1] + self._coin_h + self._coins_y_gap + self._coin_border_offset[1])
        screen.blit(self._drawing_bg, position)
        screen.blit(self._targ_coin_miniature, targ_coin_position)
        screen.blit(self._faith_coin_miniauture, faith_coin_position)

        targ_text = f"{self._currencies_info[CoinsKinds.TARGARYEN_COIN.name]:06d}"
        targ_text_surf = self._font.render(targ_text, True, self._text_color)
        targ_text_pos = (targ_coin_position[0] + self._coin_w + self._coin_text_offset[0],
                         targ_coin_position[1] + self._coin_text_offset[1])

        faith_text = f"{self._currencies_info[CoinsKinds.FAITH_COIN.name]:06d}"
        faith_text_surf = self._font.render(faith_text, True, self._text_color)
        faith_text_pos = (faith_coin_position[0] + self._coin_w + self._coin_text_offset[0],
                          faith_coin_position[1] + self._coin_text_offset[1])
        screen.blit(targ_text_surf, targ_text_pos)
        screen.blit(faith_text_surf, faith_text_pos)

    @property
    def targ_coins_balance(self):
        return self._currencies_info[CoinsKinds.TARGARYEN_COIN.name]

    @property
    def faith_coins_balance(self):
        return self._currencies_info[CoinsKinds.FAITH_COIN.name]

    def dump_into_file(self) -> None:
        with open(self._config_path, 'w') as file:
            json.dump(self._currencies_info, file)

    def spend_coins(self, coin_kind, amount) -> None:
        self._currencies_info[coin_kind.name] -= amount
        self.dump_into_file()

    def record_coin_pick(self, coin_kind: CoinsKinds, amount=1) -> None:
        self._currencies_info[coin_kind.name] += amount
        self.dump_into_file()

    def _init_from_file(self) -> None:
        if not os.path.exists(self._config_path):
            self.dump_into_file()
        else:
            with open(self._config_path) as file:
                self._currencies_info = json.load(file)