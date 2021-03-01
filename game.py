from enum import Enum, auto
from menu import Menu
from education import Education
import pygame
from game_state import GameState
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

    def draw(self):
        if self.state == GameState.MENU:
            self.menu.draw(self.screen)
        elif self.state == GameState.EDUCATION:
            self.education.draw(self.screen)

    def update(self):
        state_to_switch = None
        if self.state == GameState.MENU:
            state_to_switch = self.menu.update()
        elif self.state == GameState.EDUCATION:
            state_to_switch = self.education.update()
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
