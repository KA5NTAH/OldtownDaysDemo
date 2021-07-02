import os
from game_enums.metals import Metals
from game_enums.coins_kinds import CoinsKinds
from game_enums.achievements_names import AchievementsNames
from game_enums.game_state import GameState
from game_enums.lvl_stage import LvlStage
from game_enums.bonuses import Bonuses
import pygame
import numpy as np

SCRIPT_DIR = os.path.dirname(__file__)
RESOURSES_DIR = os.path.join(SCRIPT_DIR, 'resourses')
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 680
DROPLET_WIDTH = 30
DROPLET_HEIGHT = 30
LINK_WIDTH = 172
LINK_HEIGHT = 114
ACH_WIDTH = 80
ACH_HEIGHT = 80
LVL_ICON_WIDTH = 80
LVL_ICON_HEIGHT = 80
# RESOURSES CONST
ACHIEVEMENTS_DIR = os.path.join(RESOURSES_DIR, 'Achievements')
EDUCATION_DIR = os.path.join(RESOURSES_DIR, 'Education')
DROPLETS_DIR = os.path.join(RESOURSES_DIR, 'Droplets')
LVL_BUTTONS_DIR = os.path.join(RESOURSES_DIR, 'LvlButtons')
BACKGROUNDS_DIR = os.path.join(RESOURSES_DIR, 'Backgrounds')
PERSISTENT_INFO_DIR = os.path.join(SCRIPT_DIR, "persistent_info")
ACHIEVEMENTS_INFO_PATH = os.path.join(PERSISTENT_INFO_DIR, "achievement_info.json")
CURRENCIES_INFO_PATH = os.path.join(PERSISTENT_INFO_DIR, "currencies_info.json")
LEVELS_CONFIGS_PATH = os.path.join(SCRIPT_DIR, "levels_parameters")
PERSISTENT_LEVEL_INFO_PATH = os.path.join(PERSISTENT_INFO_DIR, "levels_info")
CURRENCIES_MANAGER_DIR = os.path.join(RESOURSES_DIR, "CurrenciesManager")
# GAME CONSTANTS
MOUSE_KEY = 0
LINKS_SWAP_THRD = 0.2
DROPLET_LINK_INTERSECTION_THRD = 1

USER_EVENT_NUM = 1


def generate_event():
    """returns new event keeping track of event num"""
    global USER_EVENT_NUM
    event = pygame.event.Event(pygame.USEREVENT + USER_EVENT_NUM)
    USER_EVENT_NUM += 1
    return event


# Events
# fixme maybe events should be in special file I'll sleep on that
GENERATE_COIN_EVENT = generate_event()
GENERATE_DROP_EVENT = generate_event()
RUINED_DROP_EVENT = generate_event()

LINK_METAL_EVENT_DICT = {}
for m in Metals:
    LINK_METAL_EVENT_DICT[m] = generate_event()
EVENT_TYPE_METAL_DICT = {}
for metal, event in LINK_METAL_EVENT_DICT.items():
    EVENT_TYPE_METAL_DICT[event.type] = metal
LINK_IS_DONE_EVENTS_TYPES = tuple(t for t in EVENT_TYPE_METAL_DICT.keys())

NO_LINK_RUIN_DICT = {}
for m in Metals:
    NO_LINK_RUIN_DICT[m] = generate_event()
EVENT_TYPE_NO_LINK_RUIN_METAL_DICT = {}
for metal, event in NO_LINK_RUIN_DICT.items():
    EVENT_TYPE_NO_LINK_RUIN_METAL_DICT[event.type] = metal
NO_LINK_RUIN_TYPES = tuple(t for t in EVENT_TYPE_NO_LINK_RUIN_METAL_DICT.keys())

LVL_EVENTS_TYPES = (GENERATE_COIN_EVENT.type,
                    GENERATE_DROP_EVENT.type,
                    RUINED_DROP_EVENT.type) + LINK_IS_DONE_EVENTS_TYPES + NO_LINK_RUIN_TYPES

# backgrounds images
LVL_BACKGROUND = pygame.image.load(os.path.join(BACKGROUNDS_DIR, 'Level_background.png'))


"""
add images for menu buttons in dict
dict should have following structure
{state: images, pos}
"""
MENU_BACKGROUND = pygame.image.load(os.path.join(BACKGROUNDS_DIR, 'Menu_background.png'))
MENU_BUTTONS_ORDER = [GameState.GAME_MODE_CHOOSING, GameState.EDUCATION, GameState.ACHIEVEMENTS, GameState.EXIT]
MENU_BUTTONS_DIR = os.path.join(RESOURSES_DIR, "MenuButtons")
MENU_BUTTONS_INFO = []
MENU_BUTTON_H = 50
MENU_BUTTON_W = 360
MENU_BUTTON_X_OFFSET = 50
MENU_BUTTON_Y_OFFSET = 50
MENU_BUTTON_Y_GAP = 10
buttons_x = np.empty(len(MENU_BUTTONS_ORDER))
buttons_x.fill(MENU_BUTTON_X_OFFSET)
buttons_y = np.arange(len(MENU_BUTTONS_ORDER)) * (MENU_BUTTON_H + MENU_BUTTON_Y_GAP) + MENU_BUTTON_Y_OFFSET
MENU_BUTTONS_POSITIONS = np.vstack((buttons_x, buttons_y)).T
for state, pos in zip(MENU_BUTTONS_ORDER, MENU_BUTTONS_POSITIONS):
    folder = os.path.join(MENU_BUTTONS_DIR, state.name)
    idle_image = pygame.image.load(os.path.join(folder, 'idle.png'))
    addressing_image = pygame.image.load(os.path.join(folder, 'addressing.png'))
    button_info = {"images": [idle_image, addressing_image], "position": pos, "state": state}
    MENU_BUTTONS_INFO.append(button_info)


# education images
EDUCATION_IMAGES = [pygame.image.load(os.path.join(EDUCATION_DIR, curr_name))
                    for curr_name in sorted(os.listdir(EDUCATION_DIR))]
EDUCATIONAL_PROGRESS_Y = 666
EDUCATIONAL_PROGRESS_RAD = 5
EDUCATIONAL_PROGRESS_X_GAP = 10
EDUCATION_SLIDES_AMOUNT = len(os.listdir(EDUCATION_DIR))
EDUCATIONAL_PROGRESS_LENGTH = EDUCATION_SLIDES_AMOUNT * EDUCATIONAL_PROGRESS_RAD * 2 \
                              + EDUCATIONAL_PROGRESS_X_GAP * (EDUCATION_SLIDES_AMOUNT - 1)
EDUCATIONAL_PROGRESS_X_START = int((1200 - EDUCATIONAL_PROGRESS_LENGTH) / 2)
EDUCATIONAL_PROGRESS_COORD = [[EDUCATIONAL_PROGRESS_X_START + EDUCATIONAL_PROGRESS_RAD * 2 * i
                               + EDUCATIONAL_PROGRESS_X_GAP * i, EDUCATIONAL_PROGRESS_Y] for i in range(EDUCATION_SLIDES_AMOUNT)]

EDUCATION_ACTIVE_COLOR = (255, 0, 0)
EDUCATION_NON_ACTIVE_COLOR = (255, 255, 255)

# bonuses images
BONUSES_DIR = os.path.join(RESOURSES_DIR, "Bonuses")
BONUSES_IMAGES = {}
for bonus in Bonuses:
    folder = os.path.join(BONUSES_DIR, bonus.name)
    idle_image = pygame.image.load(os.path.join(folder, 'idle.png'))
    selected_image = pygame.image.load(os.path.join(folder, 'selected.png'))
    img_dict = {'idle': idle_image, 'selected': selected_image}
    BONUSES_IMAGES[bonus] = img_dict


ACHIEVEMENTS_BACKGROUND = pygame.image.load(os.path.join(BACKGROUNDS_DIR, "Achievements_background.png"))
ACHIEVEMENT_ICON_POS = (200, 175)
ACHIEVEMENT_DESCRIPTION_POS = (447, 175)
ACHIEVEMENT_X_START = 60
ACHIEVEMENT_Y_START = 50
ACHIEVEMENT_X_GAP = 20
ACHIEVEMENT_Y_GAP = 20
ACHIEVEMENT_X_STOP = SCREEN_WIDTH - ACH_WIDTH - ACHIEVEMENT_X_GAP
ACHIEVEMENT_Y_STOP = SCREEN_HEIGHT - ACH_HEIGHT - ACHIEVEMENT_Y_GAP
x = np.arange(ACHIEVEMENT_X_START, ACHIEVEMENT_X_STOP + 1, ACH_WIDTH + ACHIEVEMENT_X_GAP)
y = np.arange(ACHIEVEMENT_Y_START, ACHIEVEMENT_Y_STOP + 1, ACH_HEIGHT + ACHIEVEMENT_Y_GAP)
xx, yy = np.meshgrid(x, y)
ACHIEVEMENT_POSITIONS = np.vstack((xx.flatten(), yy.flatten())).T


ACHIEVEMENTS_IMAGES = {}
for achievement in AchievementsNames:
    ach_dir = os.path.join(ACHIEVEMENTS_DIR, achievement.name)
    if os.path.exists(ach_dir):
        small_icon_locked = pygame.image.load(os.path.join(ach_dir, 'SmallIconGs.png'))
        small_icon_unlocked = pygame.image.load(os.path.join(ach_dir, 'SmallIcon.png'))
        big_icon_locked = pygame.image.load(os.path.join(ach_dir, 'BigIconGs.png'))
        big_icon_unlocked = pygame.image.load(os.path.join(ach_dir, 'BigIcon.png'))
        description = pygame.image.load(os.path.join(ach_dir, 'Description.png'))
        ACHIEVEMENTS_IMAGES[achievement] = [small_icon_locked,
                                          small_icon_unlocked,
                                          big_icon_locked,
                                          big_icon_unlocked,
                                          description]


MODE_SELECTION_BACKGROUND = pygame.image.load(os.path.join(BACKGROUNDS_DIR, "Mode_choosing_background.png"))
MODE_SELECTION_BUTTONS_INFO = []
mode_buttons_folder = os.path.join(RESOURSES_DIR, 'Mode_selection')
selection_positions = [[60, 60], [660, 60]]
for state, pos in zip([GameState.INFINITE_PLAY, GameState.LEVEL_CHOOSING], selection_positions):
    folder = os.path.join(mode_buttons_folder, state.name)
    idle_image = pygame.image.load(os.path.join(folder, 'idle.png'))
    active_image = pygame.image.load(os.path.join(folder, 'selected.png'))
    images = [idle_image, active_image]
    MODE_SELECTION_BUTTONS_INFO.append({"images": images, "position": pos, "state": state})


FATHERS_JUDGEMENT_THRD = 0.5
FATHERS_PUNISHMENT = 100  # amount of coins to be disposed of
TRIAL_BONUSES_IMAGES = {}
"""
structure is:
bonus_name:
    - roll image
    - with_description.png
"""


LVL_SHOOSING_BACKGROUND = pygame.image.load(os.path.join(BACKGROUNDS_DIR, "Level_choosing_background.png"))
LVL_BUTTONS_X_START = 60
LVL_BUTTONS_Y_START = 50
LVL_BUTTONS_X_GAP = 20
LVL_BUTTONS_Y_GAP = 20
LVL_BUTTONS_X_STOP = 884 - LVL_ICON_WIDTH - ACHIEVEMENT_X_GAP
LVL_BUTTONS_Y_STOP = SCREEN_HEIGHT - LVL_ICON_HEIGHT - ACHIEVEMENT_Y_GAP
x = np.arange(LVL_BUTTONS_X_START, LVL_BUTTONS_X_STOP + 1, LVL_ICON_WIDTH + LVL_BUTTONS_X_GAP)
y = np.arange(LVL_BUTTONS_Y_START, LVL_BUTTONS_Y_STOP + 1, LVL_ICON_HEIGHT + LVL_BUTTONS_Y_GAP)
xx, yy = np.meshgrid(x, y)
LVL_BUTTONS_POSITIONS = np.vstack((xx.flatten(), yy.flatten())).T


LVL_BUTTONS_INFO = []
LOCKED_LEVEL_IMAGE = pygame.image.load(os.path.join(LVL_BUTTONS_DIR, 'LvlCloseIcon.png'))
for folder_name, pos in zip(sorted(os.listdir(LVL_BUTTONS_DIR)), LVL_BUTTONS_POSITIONS):
    folder_path = os.path.join(LVL_BUTTONS_DIR, folder_name)
    if not os.path.isdir(folder_path):
        continue
    idle_image = pygame.image.load(os.path.join(folder_path, 'idle.png'))
    selected_image = pygame.image.load(os.path.join(folder_path, 'selected.png'))
    LVL_BUTTONS_INFO.append({"images": [idle_image, selected_image], "position": pos, "lvl_num": int(folder_name)})



# Challenge
CHALLENGE_TARGET_RADIUS = 30
CHALLENGE_TIMER_LINE_WIDTH = 20
CHALLENGE_FOLDER = os.path.join(RESOURSES_DIR, 'Challenge')
CHALLENGE_IMAGES = {}
""" 
expected challenge folder structure
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
four_links_arrangement = five_links_arrangement[:-1]
three_links_arrangement = five_links_arrangement[1:-1]
two_links_arrangement = five_links_arrangement[[1, 3]]
one_link_arrangement = np.array([five_links_arrangement[[2]]])
LINKS_COORDINATES = {
    1: one_link_arrangement,
    2: two_links_arrangement,
    3: three_links_arrangement,
    4: four_links_arrangement,
    5: five_links_arrangement
}


DROPLETS_IMAGES = {}
for metal in Metals:
    droplet_path = os.path.join(DROPLETS_DIR, f'{metal.name}.png')
    if not os.path.exists(droplet_path):
        continue
    DROPLETS_IMAGES[metal] = pygame.image.load(droplet_path)


# Load coins images
COINS_FOLDER = os.path.join(RESOURSES_DIR, "Coins")
COINS_IMAGES = {}
for coin_kind in CoinsKinds:
    COINS_IMAGES[coin_kind] = pygame.image.load(os.path.join(COINS_FOLDER, f'{coin_kind.name}.png'))


COINS_RADIUS = 35
COINS_WIDTH = 70
COINS_HEIGHT = 70
COINS_EDGE_OFFSET = 100
COINS_X_BOUNDARIES = (COINS_WIDTH + COINS_EDGE_OFFSET, SCREEN_WIDTH - COINS_EDGE_OFFSET)
COINS_Y_BOUNDARIES = (COINS_HEIGHT + COINS_EDGE_OFFSET, links_y - COINS_EDGE_OFFSET)



# MODE_SELECTION_BUTTONS_INFO.append({"images": images, "position": pos, "state": state})
# fixme maybe buttons should be initialized by one function Seems like process can standardized
loser_options_dir = os.path.join(RESOURSES_DIR, "LoserOptionsButtons")
LOSER_OPTIONS_BACKGROUND = pygame.image.load(os.path.join(BACKGROUNDS_DIR, "Loser_options_background.png"))
loser_buttons_positions = {"bribe": [60, 80],
                           "menu": [443, 80],
                           "trial": [826, 80]}
BRIBE_COST = 250
TRIAL_OF_THE_SEVEN_COST = 50


LOSER_BUTTONS_INFO = {}
# init buttons
bribe_folder = os.path.join(loser_options_dir, "bribe")
for folder in os.listdir(loser_options_dir):
    if folder != "menu":
        idle_img = pygame.image.load(os.path.join(loser_options_dir, folder, "idle.png"))
        closed_img = pygame.image.load(os.path.join(loser_options_dir, folder, "closed.png"))
        opened_img = pygame.image.load(os.path.join(loser_options_dir, folder, "opened.png"))
        images = [idle_img, closed_img, opened_img]
    else:
        idle_img = pygame.image.load(os.path.join(loser_options_dir, folder, "idle.png"))
        addressing_img = pygame.image.load(os.path.join(loser_options_dir, folder, "addressing.png"))
        images = [idle_img, addressing_img]
    LOSER_BUTTONS_INFO[folder] = {"images": images, "position": loser_buttons_positions[folder]}


# WINNER OPTIONS
# load images
WINNER_OPTIONS_FOLDER = os.path.join(RESOURSES_DIR, "WinnerOptionsButtons")
WINNER_OPTIONS_BACKGROUND = pygame.image.load(os.path.join(BACKGROUNDS_DIR, "Winner_options_background.png"))
back_to_level_images = [pygame.image.load(os.path.join(WINNER_OPTIONS_FOLDER, "back_to_levels", img_name))
                        for img_name in ("idle.png", "addressing.png")]
next_level_images = [pygame.image.load(os.path.join(WINNER_OPTIONS_FOLDER, "next_level", img_name))
                     for img_name in ("idle.png", "addressing.png")]
WINNER_OPTIONS_INFO = {"back_to_menu": {"images": back_to_level_images,
                                        "position": [227, 80]},
                       "next_level": {"images": next_level_images,
                                      "position": [659, 80]}}

# PROGRESS BARS
WINNING_BAR_POSITION = (1115, 397)
LOSING_BAR_POSITION = (1158, 397)
LEVEL_BARS_INNER_PART_OFFSET = (5, 5)
PROGRESS_BAR_FOLDER = os.path.join(RESOURSES_DIR, "ProgressBars")
PROGRESS_BAR_IMAGES = {}
for bar_name in ("winning", "losing"):
    bar_folder = os.path.join(PROGRESS_BAR_FOLDER, bar_name)
    PROGRESS_BAR_IMAGES[bar_name] = [pygame.image.load(os.path.join(bar_folder, "background.png")),
                                     pygame.image.load(os.path.join(bar_folder, "empty.png")),
                                     pygame.image.load(os.path.join(bar_folder, "filled.png"))]


GENERAL_FOLDER = os.path.join(RESOURSES_DIR, "General")
EMPTY_LINK_FILLER = pygame.image.load(os.path.join(GENERAL_FOLDER, "empty_link_filler.png"))


# TRIAL OF THE SEVEN BACKGROUNDS
TRIAL_BG_FOLDER = os.path.join(RESOURSES_DIR, "TrialBackgrounds")
TRIAL_BACKGROUNDS = {}
for god in Bonuses:
    if god == Bonuses.FATHER:
        TRIAL_BACKGROUNDS[god] = {"positive": pygame.image.load(os.path.join(TRIAL_BG_FOLDER, f"{god.name}_POS.png")),
                                  "negative": pygame.image.load(os.path.join(TRIAL_BG_FOLDER, f"{god.name}_NEG.png"))}
    else:
        TRIAL_BACKGROUNDS[god] = pygame.image.load(os.path.join(TRIAL_BG_FOLDER, f"{god.name}.png"))

TRIAL_BUTTON_POSITION = (60, 574)
TRIAL_BUTTON_FOLDER = os.path.join(RESOURSES_DIR, "TrialButton")
TRIAL_BUTTON_IMAGES = [pygame.image.load(os.path.join(TRIAL_BUTTON_FOLDER, "idle.png")),
                       pygame.image.load(os.path.join(TRIAL_BUTTON_FOLDER, "addressing.png"))]

# Currencies Manager
TARG_COIN_MINIATURE = pygame.image.load(os.path.join(CURRENCIES_MANAGER_DIR, "targ_miniature.png"))
FAITH_COIN_MINIATURE = pygame.image.load(os.path.join(CURRENCIES_MANAGER_DIR, "faith_miniature.png"))
CURRENCIES_MANAGER_BG = pygame.image.load(os.path.join(CURRENCIES_MANAGER_DIR, "bg.png"))
