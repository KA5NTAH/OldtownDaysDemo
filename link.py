import pygame
import os
from game_enums.link_stage import LinkStage
from game_enums.metals import Metals
from expiring_object import ExpiringObject
from responsive_objects.mouse_responsive import MouseResponsive
from responsive_objects.rectangle_responsive import RectangleResponsive
import sys
pygame.init()


class Link(RectangleResponsive, MouseResponsive, ExpiringObject):
	""" Link main task is to keep track of its state """  # fixme
	def __init__(self, empty_img, full_img, timer_img, position, time, metal):
		self._stage = LinkStage.FILLING
		self._empty_img = empty_img
		self._full_img = full_img
		self._timer_img = timer_img
		self._drawing_position = position
		self._metal = metal
		_, _, w, h = self._empty_img.get_rect()
		self._filling_rate = 1  # fixme maybe it should be parameter of __init__
		self._filled_lvl = 0
		self._height = h
		super().__init__(pygame.Rect(*self._drawing_position, w, h), 0)
		self._rect = self._addressing_rect
		ExpiringObject.__init__(self, time)  # fixme there might be something wrong

	@property
	def stage(self):
		return self._stage

	@property
	def rect(self):
		return self._rect

	@property
	def metal(self):
		return self._metal

	def put_into_place(self):
		self._rect = self._addressing_rect

	def move(self, vector):
		self._rect = self._rect.move(vector)

	def draw(self, screen):
		if self._stage == LinkStage.FILLING or self._stage == LinkStage.CHALLENGE_PROPOSAL:
			if self._stage == LinkStage.FILLING:
				lower_part = self._full_img
				upper_part = self._empty_img
				surface_y = self._height - self._filled_lvl
			elif self._stage == LinkStage.CHALLENGE_PROPOSAL:
				lower_part = self._timer_img
				upper_part = self._full_img
				surface_y = int(self._height * self._ttl / self._life_time)
			"""
			A ----- *
			|       |
			C ----- B
			|       |
			* ----- D
			"""
			A = (0, 0)
			B = (self._rect.width, surface_y)
			C = (0, surface_y)
			D = (self._rect.width, self._height)
			start_pos = (self._rect.left, self._rect.top)
			screen.blit(upper_part, start_pos, (*A, *B))
			screen.blit(lower_part, (start_pos[0], start_pos[1] + surface_y), (*C, *D))

	def pour_metal(self):
		self._filled_lvl = min(self._height, self._filled_lvl + self._filling_rate)

	def update(self):
		""" If Link is filled than it should go into challenge proposal stage
		if it is in challenge proposal state then see if it is expired already"""
		if self._stage == LinkStage.FILLING:
			if self._filled_lvl == self._height:
				self._refresh_clock()
				self._stage = LinkStage.CHALLENGE_PROPOSAL
		elif self._stage == LinkStage.CHALLENGE_PROPOSAL:
			self.update_ttl()
			if not self.is_still_alive():
				self._stage = LinkStage.DONE
