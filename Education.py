import pygame
from Game import GameState
from enum import Enum, auto
import sys
import os
from os.path import join as opj
from collections import deque
from Link import Link
from channel import Channel
import utils
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
        self.stages_flow = self.stages
        self.images = deque(EDUCATION_IMAGES)
        self.curr_stage = self.stages_flow.popleft()
        self.curr_image = self.images.popleft()
        # init space key state
        pressed_keys = pygame.key.get_pressed()
        self.old_space = pressed_keys[pygame.K_SPACE]
    
    def go_to_next_stage(self):
        if self.stages_flow:
            self.curr_stage = self.stages_flow.popleft()
        if self.images:
            self.curr_image = self.images.popleft()

    def draw(self, screen):
        # todo organise this into queue
        screen.blit(self.curr_image, (0, 0))

    def update(self):
        """
        update should track actions and update objects states and decide id we should move to the next stage
        """
        pressed_keys = pygame.key.get_pressed()
        curr_space = pressed_keys[pygame.K_SPACE]
        if curr_space and not self.old_space:
            self.go_to_next_stage()
        self.old_space = curr_space


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
