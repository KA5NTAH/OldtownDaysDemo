import pygame
import utils
from enum import Enum, auto
import sys
import os
from os.path import join as opj
from game_state import GameState
SCRIPT_DIR = os.path.dirname(__file__)
pygame.init()


# todo rework with buttons
class EnumFromZero(Enum):
    def __new__(cls, *args):
        value = len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class MenuState(EnumFromZero):
    PLAY = auto()
    EDUCATION = auto()
    ACHIEVEMENTS = auto()
    SETTINGS = auto()
    EXIT = auto()


EDUCATION_IMFOLDER = opj(SCRIPT_DIR, 'resourses', 'Menu')


class Menu:
    def __init__(self):
        self.menu_options_dict = self._init_options_dict()
        self.all_options = list(MenuState)
        self.curr_option = MenuState.PLAY
        pressed_keys = pygame.key.get_pressed()
        self.old_up = pressed_keys[pygame.K_UP]
        self.old_down = pressed_keys[pygame.K_DOWN]
        self.old_space = pressed_keys[pygame.K_SPACE]
        self.game_state_mapping = {MenuState.PLAY: GameState.PLAY,
                                   MenuState.EDUCATION: GameState.EDUCATION,
                                   MenuState.ACHIEVEMENTS: GameState.ACHIEVEMENTS,
                                   MenuState.SETTINGS: GameState.SETTINGS,
                                   MenuState.EXIT: GameState.EXIT}

    def _init_options_dict(self):
        options_dict = {}
        for state in list(MenuState):
            impath = opj(EDUCATION_IMFOLDER, f'{state.name}.png')
            image = pygame.image.load(impath)
            options_dict[state] = image
        return options_dict

    def draw(self, screen):
        screen.blit(self.menu_options_dict[self.curr_option], (0, 0))

    def update(self) -> GameState:
        dst_game_state = None
        pressed_keys = pygame.key.get_pressed()
        curr_up = pressed_keys[pygame.K_UP]
        curr_down = pressed_keys[pygame.K_DOWN]
        curr_space = pressed_keys[pygame.K_SPACE]
        curr_option_num = self.curr_option.value
        if curr_up and not self.old_up:
            curr_option_num = (curr_option_num - 1) % len(self.all_options)
            self.curr_option = MenuState(curr_option_num)
        if curr_down and not self.old_down:
            curr_option_num = (curr_option_num + 1) % len(self.all_options)
            self.curr_option = MenuState(curr_option_num)
        if curr_space and not self.old_space:
            dst_game_state = self.game_state_mapping[self.curr_option]
        self.old_up = curr_up
        self.old_down = curr_down
        self.old_space = curr_space
        return dst_game_state


# todo delete this local tests
if __name__ == '__main__':
    width, height = 1000, 800
    black = (0, 0, 0)
    size = (width, height)
    screen = pygame.display.set_mode(size)
    m = Menu()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(black)
        # update block
        m.update()
        # draw block
        m.draw(screen)
        pygame.display.flip()
