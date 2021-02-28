import os
import matplotlib.pyplot as plt
import pygame
import sys
# todo move to consts file
GOLDEN_COLOR = "gold"
BLACK_IRON_COLOR = "black_iron"
SCRIPT_DIR = os.path.dirname(__file__)


def get_lines_overlapping(line1, line2):
	"""
	a ------ b
		c ---------d
	"""
	a, b = line1
	c, d = line2
	if a > c:
		a, b = line2
		c, d = line1
	common_area = b - c
	common_area = max(common_area, 0)
	common_area = min(common_area, d - c)
	return common_area


def get_intersection(bb1, bb2):
	left1, top1, w1, h1 = bb1
	left2, top2, w2, h2 = bb2
	common_height = get_lines_overlapping((top1, top1 + h1), (top2, top2 + h2))
	common_width = get_lines_overlapping((left1, left1 + w1), (left2, left2 + w2))
	intersection = common_width * common_height
	return intersection


def get_iou(bb1, bb2):
	intersection = get_intersection(bb1, bb2)
	s1 = bb1.width * bb1.height
	s2 = bb2.width * bb2.height
	union = s1 + s2 - intersection
	return intersection / union


def load_images_by_metal_key(metal_key):
	# demo version for two links
	filled_img = None
	if metal_key == GOLDEN_COLOR:
		filled_img = pygame.image.load(os.path.join(SCRIPT_DIR, "resourses", "golden_ref.png"))
	elif metal_key == BLACK_IRON_COLOR:
		filled_img = pygame.image.load(os.path.join(SCRIPT_DIR, "resourses", "black_iron_ref.png"))
	empty_img = pygame.image.load(os.path.join(SCRIPT_DIR, "resourses", "empty_ref.png"))
	return empty_img, filled_img


def set_gs_to_set():
	from Game import Game, GameState
	Game.switch_state(GameState.SETTINGS)


if __name__ == "__main__":
	rect = pygame.Rect(75, 0, 50, 50)
	rect1 = pygame.Rect(0, 567, 200, 133)
	print(get_intersection(rect, rect1))
	for i in range(1000):
		rect = rect.move(0, 1)
		if get_intersection(rect, rect1) > 0:
			print(rect)

