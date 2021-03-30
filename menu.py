import pygame
import sys
import os
import game_constants
from game_enums.game_state import GameState
from game_enums.menu_state import MenuState
from responsive_objects.button import Button


class Menu:
    def __init__(self):
        self.menu_game_state_mapping = {MenuState.PLAY: GameState.PLAY,
                                        MenuState.EDUCATION: GameState.EDUCATION,
                                        MenuState.ACHIEVEMENTS: GameState.ACHIEVEMENTS,
                                        MenuState.EXIT: GameState.EXIT}

    def _init_buttons(self):
        positions = []
        # todo init images in constants
        buttons = []
        for pos, state in zip(positions, MenuState):
            images = []
            button = Button(*images, pos, game_constants.MOUSE_KEY)

    def update_and_return_selected_mode(self) -> GameState:
        pass

    def draw(self, screen):
        # todo draw some background
        pass


# todo delete this local tests
if __name__ == '__main__':
    pygame.init()
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
