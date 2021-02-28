import pygame
from enum import Enum, auto
import sys
import os
from os.path import join as opj
from collections import deque
from link import Link
from channel import Channel
import utils
from game_state import GameState
pygame.init()
SCRIPT_DIR = os.path.dirname(__file__)


class EducationState(Enum):
    MainMechanics = auto()
    MainMechanicsPress = auto()
    MainMechanicsMove = auto()
    MainMechanicsRelease = auto()
    Challenge = auto()
    GameCurrencies = auto()
    CurrenciesUsage = auto()
    JudgementOfTheSeven = auto()
    # todo add all seven gods arts (maybe just all gods combined in one art)
    EndEducation = auto()


EDUCATION_IMFOLDER = opj(SCRIPT_DIR, 'resourses', 'Education')
EDUCATION_IMAGES = []
for state in list(EducationState):
    impath = opj(EDUCATION_IMFOLDER, f'{state.name}.png')
    image = pygame.image.load(impath)
    EDUCATION_IMAGES.append(image)


class Education:
    def __init__(self):
        self.stages = deque(list(EducationState))
        self.stages_flow = deque(self.stages)
        self.images = deque(EDUCATION_IMAGES)
        self.curr_stage = self.stages_flow.popleft()
        self.curr_image = self.images.popleft()
        # init space key state
        pressed_keys = pygame.key.get_pressed()
        self.old_space = pressed_keys[pygame.K_SPACE]
        self.exit_game_state = GameState.MENU

    def set_education_to_start(self):
        self.stages_flow = deque(self.stages)
        self.images = deque(EDUCATION_IMAGES)
        self.curr_stage = self.stages_flow.popleft()
        self.curr_image = self.images.popleft()

    def go_to_next_stage(self):
        if self.stages_flow:
            self.curr_stage = self.stages_flow.popleft()
        if self.images:
            self.curr_image = self.images.popleft()

    def draw(self, screen):
        # todo organise this into queue
        screen.blit(self.curr_image, (0, 0))

    def update(self) -> GameState:
        dst_game_state = None
        """
        update should track actions and update objects states and decide id we should move to the next stage
        """
        pressed_keys = pygame.key.get_pressed()
        curr_space = pressed_keys[pygame.K_SPACE]
        if curr_space and not self.old_space:
            if self.curr_stage == EducationState.EndEducation:
                dst_game_state = self.exit_game_state
                self.set_education_to_start()
            else:
                self.go_to_next_stage()
        self.old_space = curr_space
        return dst_game_state


# todo delete this local tests
if __name__ == '__main__':
    width, height = 1000, 800
    black = (0, 0, 0)
    size = (width, height)
    screen = pygame.display.set_mode(size)
    ed = Education()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(black)
        # update block
        ed.update()
        # draw block
        ed.draw(screen)

        pygame.display.flip()
