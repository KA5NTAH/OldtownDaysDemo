import os

DROPLET_WIDTH = 30
DROPLET_HEIGHT = 30
LINK_WIDTH = 172
LINK_HEIGHT = 114
SCRIPT_DIR = os.path.dirname(__file__)
SCRIPT_DIR = os.path.dirname(__file__)
RESOURSES_DIR = os.path.join(SCRIPT_DIR, 'resourses')
ACHIEVEMENTS_DIR = os.path.join(RESOURSES_DIR, 'Achievements')
DROPLETS_DIR = os.path.join(RESOURSES_DIR, 'Droplets')
LINKS_DIR = os.path.join(RESOURSES_DIR, 'Links')
print(os.listdir(LINKS_DIR))
