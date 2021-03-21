import os
from game_enums.metals import Metals
import pygame
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__)
RESOURSES_DIR = os.path.join(SCRIPT_DIR, 'resourses')
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680
DROPLET_WIDTH = 30
DROPLET_HEIGHT = 30
LINK_WIDTH = 172
LINK_HEIGHT = 114
# RESOURSES CONST
ACHIEVEMENTS_DIR = os.path.join(RESOURSES_DIR, 'Achievements')
DROPLETS_DIR = os.path.join(RESOURSES_DIR, 'Droplets')
LINKS_DIR = os.path.join(RESOURSES_DIR, 'Links')

# GAME CONSTANTS
MOUSE_KEY = 0
LINKS_SWAP_THRD = 0.5

# Events fixme maybe events should be in special file
GENERATE_COIN_EVENT = pygame.USEREVENT + 1
GENERATE_DROP_EVENT = pygame.USEREVENT + 2


# Challenge
CHALLENGE_TARGET_RADIUS = 30
CHALLENGE_TIMER_LINE_WIDTH = 20
CHALLENGE_FOLDER = os.path.join(RESOURSES_DIR, 'Challenge')
CHALLENGE_IMAGES = {}
""" expected challenge folder structure
- metal_key
    background_image.png
    - 001 
        - trace_image.png
        - idle_image.png
        - calling_image.png
    - 002
        - trace_image.png
        - idle_image.png
        - calling_image.png
    ....
....    
"""

for metal in Metals:
    curr_info_dict = {}
    challenge_sub_folder = os.path.join(CHALLENGE_FOLDER, metal.name)
    if not os.path.exists(challenge_sub_folder):
        continue
    bg_img = pygame.image.load(os.path.join(challenge_sub_folder, 'background_image.png'))
    curr_info_dict['bg_img'] = bg_img

    targets_sub_folders = sorted(os.path.join(challenge_sub_folder, f) for f in os.listdir(challenge_sub_folder))
    targets_sub_folders = filter(lambda path: os.path.isdir(path), targets_sub_folders)
    targets_images = []
    for target_folder in targets_sub_folders:
        trace_image_path = os.path.join(target_folder, 'trace_image.png')
        idle_image_path = os.path.join(target_folder, 'idle_image.png')
        calling_image_path = os.path.join(target_folder, 'calling_image.png')
        curr_images = [pygame.image.load(trace_image_path),
                       pygame.image.load(idle_image_path),
                       pygame.image.load(calling_image_path)]
        targets_images.append(curr_images)
    curr_info_dict['targets_images'] = targets_images
    CHALLENGE_IMAGES[metal] = curr_info_dict

# Links
LINKS_DIR = os.path.join(RESOURSES_DIR, 'Links')
"""
Links dir structure:
Links:
    Metal:
        Empty.png
        Full.png
        FullTimer.png
    Metal2
        ...
    ...
"""

LINKS_IMAGES = {}
for metal in Metals:
    link_dir = os.path.join(LINKS_DIR, metal.name)
    if not os.path.exists(link_dir):
        continue
    empty_img_path = os.path.join(link_dir, 'Empty.png')
    full_img_path = os.path.join(link_dir, 'Full.png')
    timer_img_path = os.path.join(link_dir, 'FullTimer.png')
    LINKS_IMAGES[metal] = [pygame.image.load(empty_img_path),
                           pygame.image.load(full_img_path),
                           pygame.image.load(timer_img_path)]

# for each number of links there is special coordinates arrangements ()
links_y = 533
five_links_x = np.arange(5) * 212 + 40
five_links_arrangement = np.vstack((five_links_x, np.ones((5,)) * links_y)).T.astype(np.int32)
LINKS_COORDINATES = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: five_links_arrangement
}


# todo add droplets images load
DROPLETS_IMAGES = {}
for metal in Metals:
    droplet_path = os.path.join(DROPLETS_DIR, f'{metal.name}.png')
    if not os.path.exists(droplet_path):
        continue
    DROPLETS_IMAGES[metal] = pygame.image.load(droplet_path)
