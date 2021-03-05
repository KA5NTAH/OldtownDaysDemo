import pygame
import os
from game_enums.link_stage import LinkStage
from game_enums.metals import Metals
from expiring_clickable_target import ExpiringClickableTarget


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


# todo some loader
def load(metal_key):
	return (0, 0, 0)


class NewLink(ExpiringClickableTarget):
	def __init__(self, metal: Metals, time: int, start_pos: tuple, finish_pos: tuple):
		super().__init__(time)
		# load images based on metal
		self._metal = metal
		empty, filled, glowing = load(self._metal)
		self._empty_img = empty
		self._filled_img = filled
		self._glowing_img = glowing
		# init rect
		self.rect = self._empty_img.get_rect()
		_, _, self.w, self.h = self.rect
		x, y = start_pos
		self.rect.left = x
		self.rect.top = y
		#
		self._filled_lvl = 0
		self._filling_rate = 1
		self._stage = LinkStage.FILLING
		# finish pos
		self._finish_pos = finish_pos

	def draw(self, screen):
		"""
		A ----- *
		|       |
		C ----- B
		|       |
		* ----- D
		"""
		# todo add logic for finished link
		if self._stage == LinkStage.FILLING or self._stage == LinkStage.CHALLENGE_PROPOSAL:
			lower_img = self._filled_img
			upper_img = self._empty_img
			if self._stage == LinkStage.CHALLENGE_PROPOSAL:
				lower_img = self._glowing_img
				upper_img = self._filled_img
			A = (0, 0)
			surface_y = self.h - self._filled_lvl
			B = (self.w, surface_y)
			C = (0, surface_y)
			D = (self.w, self.h)

			start_pos = (self.rect.left, self.rect.top)
			screen.blit(upper_img, start_pos, (*A, *B))
			screen.blit(lower_img, (start_pos[0], start_pos[1] + surface_y), (*C, *D))
		else:
			screen.blit(self._filled_img, self._finish_pos)

	# ensure that stage is  updated
	def update(self):
		if self._stage == LinkStage.FILLING:
			if self.is_filled():
				self._stage = LinkStage.CHALLENGE_PROPOSAL
		elif self._stage == LinkStage.CHALLENGE_PROPOSAL:
			self.update_ttl()
			if not self.is_still_alive():
				self._stage = LinkStage.DONE

	@property
	def filling_rate(self):
		return self._filling_rate

	@filling_rate.setter
	def filling_rate(self, value):
		self.filling_rate = min(value, self.h)

	@property
	def metal(self):
		return self._metal

	def move(self, vector):
		self.rect = self.rect.move(vector)

	def pour_metal_drop(self):
		self._filled_lvl += 1
		self._filled_lvl = min(self.h, self._filled_lvl)

	def is_filled(self):
		return self.h == self._filled_lvl

	def make_empty(self):
		self._filled_lvl = 0

	def _is_mouse_inside(self) -> bool:
		x, y = pygame.mouse.get_pos()
		left, top, w, h = self.rect
		return left <= x <= left + w and top <= y <= top + h

	def _get_user_action(self) -> bool:
		button_state, _, _ = pygame.mouse.get_pressed()
		return button_state

	def fit_link_to_width(self, width):
		pass

	def fit_link_to_height(self, height):
		pass
