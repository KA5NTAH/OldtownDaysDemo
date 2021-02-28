import pygame
import os


class Link:
	def __init__(self, start_pos, empty_img, filled_img, metal_key):
		self._filled_img = filled_img
		self._empty_img = empty_img
		self.rect = empty_img.get_rect()
		_, _, self.w, self.h = self.rect
		x, y = start_pos
		self.rect.left = x
		self.rect.top = y		

		self._filled_lvl = 0
		self._filling_rate = 1  # allow user to set this value
		self._metal_key = metal_key

		# check that images are same
		_, _, tw, th = filled_img.get_rect()
		# todo raise error if w, h differ
		if (self.w != tw) or (self.h != th):
			print("Erorr images arent same")

	# todo use property decorator
	def set_fill_rate(self, value):
		self._filling_rate = min(self.h, value)

	def check_metal_compatibility(self, ball):
		return self._metal_key == ball._metal_key

	def is_filled(self):
		return self.h == self._filled_lvl

	def make_empty(self):
		self._filled_lvl = 0

	def fill(self):
		self._filled_lvl += self._filling_rate
		self._filled_lvl = min(self.h, self._filled_lvl)

	def move(self, vector):
		self.rect = self.rect.move(vector)

	def draw(self, screen):
		"""
		A ----- *
		|       |
		C ----- B
		|       |
		* ----- D
		"""
		A = (0, 0)
		surface_y = self.h - self._filled_lvl
		B = (self.w, surface_y)
		C = (0, surface_y)
		D = (self.w, self.h)

		start_pos = (self.rect.left, self.rect.top)
		screen.blit(self._empty_img, start_pos, (*A, *B))
		screen.blit(self._filled_img,
					(start_pos[0], start_pos[1] + surface_y), (*C, *D))
