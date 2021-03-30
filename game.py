from enum import Enum, auto
from menu import Menu
from education import Education
import pygame
from game_enums.game_state import GameState
import sys
import os


class Game:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 800
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.menu = Menu()
        self.education = Education()
        self.state = GameState.MENU
        # todo maybe it would be more suitable to use dict for getting object that should be updated or drawn
        self.state_object_mapping = {}
        # todo maybe it would be more suitable to use dict or getting that should update or drawn
        self.state_object_mapping = {GameState.MENU: self.menu,
                                     GameState.EDUCATION: self.education}
        # todo create screen of our own

    def draw(self):
        self.state_object_mapping[self.state].draw(self.screen)

    def update(self):
        state_to_switch = self.state_object_mapping[self.state].update()
        if state_to_switch is not None:
            self.state = state_to_switch

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill((0, 0, 0))
            # update block
            self.update()
            # draw block
            self.draw()
            pygame.display.flip()


app = Game()
app.run()
