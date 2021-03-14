import numpy as np
import time
import os
import sys
from os.path import join as opj
import pygame
from responsive_objects.button import Button
SCRIPT_DIR = os.path.dirname(__file__)
pygame.init()


idle = pygame.image.load(opj(SCRIPT_DIR, 'resourses', 'Menu', 'idle_test.png'))
active = pygame.image.load(opj(SCRIPT_DIR, 'resourses', 'Menu', 'active_test.png'))


AchievementName = "LordOfCasterlyRock"
icon = pygame.image.load(f"C:\\Users\\ААА\\Desktop\\Будни Староместа\\achievements\\{AchievementName}\\SmallGrayScale.png")
description = pygame.image.load(f"C:\\Users\\ААА\\Desktop\\Будни Староместа\\achievements\\{AchievementName}\\Description.png")

if __name__ == '__main__':
    width, height = 1200, 680
    black = (255, 255, 255)
    size = (width, height)
    screen = pygame.display.set_mode(size)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(black)
        screen.blit(icon, (200, 175))
        screen.blit(description, (447, 175))
        pygame.display.flip()

