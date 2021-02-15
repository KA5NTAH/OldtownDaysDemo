import pygame
import pygame.gfxdraw
import numpy as np
import time
import sys
import os
import matplotlib.pyplot as plt
from os.path import join as opj
from Link import Link
SCRIPT_DIR = os.path.dirname(__file__)
print(SCRIPT_DIR)

img_path = os.path.join(SCRIPT_DIR, "targ_sigil.jpg")

size = width, height = 1000, 800
speed = [2, 2]
black = (0, 0, 0)
green = (0, 255, 0)
screen = pygame.display.set_mode(size)
time = 5

CLOSE_DOOR = pygame.USEREVENT + 1
pygame.time.set_timer(CLOSE_DOOR, time)
black_color = True
cx = int(width / 2) - 230
cy = int(height / 2) - 120	


# todo 
def test_link():
	golden_link = pygame.image.load(opj(SCRIPT_DIR, "black_iron_ref.png"))
	empty_link = pygame.image.load(opj(SCRIPT_DIR, "empty_ref.png"))
	rect = empty_link.get_rect()
	link_of_gold = Link((cx, cy), empty_link, golden_link, 1)
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == CLOSE_DOOR:
				link_of_gold.fill()
				# link_of_gold.move((1, -1))
		screen.fill(black)
		if link_of_gold.is_filled():
			link_of_gold.make_empty()
		link_of_gold.draw(screen)
		pygame.display.flip()


test_link()	
