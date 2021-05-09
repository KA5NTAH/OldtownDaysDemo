import os
import matplotlib.pyplot as plt
import pygame
import sys
from responsive_objects.button import Button
from game_enums.user_intention import UserIntention


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


def init_buttons_from_info(button_info, command_creator, mouse_key):
	buttons = []
	for button_info in button_info:
		images = button_info["images"]
		position = button_info["position"]
		command = command_creator(button_info)
		button = Button(*images, position, mouse_key, command)
		buttons.append(button)
	return buttons


def process_buttons(buttons):
	for index in range(len(buttons)):
		user_intention = buttons[index].get_user_intention_and_update_track()
		if user_intention == UserIntention.SWITCH_OFF:
			buttons[index].click()


if __name__ == "__main__":
	pass

