import pygame
import os
from game_enums.link_stage import LinkStage
from game_enums.metals import Metals
from expiring_object import ExpiringObject
from responsive_objects.mouse_responsive import MouseResponsive
from responsive_objects.rectangle_responsive import RectangleResponsive
import sys
from game_constants import LINK_METAL_EVENT_DICT


class Link(RectangleResponsive, MouseResponsive, ExpiringObject):
	""" Link main task is to keep track of its state """  # fixme doc string
	def __init__(self, empty_img, full_img, timer_img, filling_rate, position, time, metal, mouse_key):
		self._stage = LinkStage.FILLING
		self._empty_img = empty_img
		self._full_img = full_img
		self._timer_img = timer_img
		self._drawing_position = position
		self._metal = metal
		_, _, w, h = self._empty_img.get_rect()
		self._filling_rate = filling_rate
		self._filled_lvl = 0
		self._height = h
		self._event_posted = False
		super().__init__(pygame.Rect(*self._drawing_position, w, h), mouse_key)
		ExpiringObject.__init__(self, time)

	# todo add event generator + make sure that event will be sent only once
	@property
	def addressing_rect(self):
		return self._addressing_rect

	@addressing_rect.setter
	def addressing_rect(self, newRect):
		self._addressing_rect = newRect

	def move(self, vector):
		self._addressing_rect = self._addressing_rect.move(vector)

	@property
	def stage(self):
		return self._stage

	@property
	def metal(self):
		return self._metal

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
			B = (self._addressing_rect.width, surface_y)
			C = (0, surface_y)
			D = (self._addressing_rect.width, self._height)
			start_pos = (self._addressing_rect.left, self._addressing_rect.top)
			screen.blit(upper_part, start_pos, (*A, *B))
			screen.blit(lower_part, (start_pos[0], start_pos[1] + surface_y), (*C, *D))

	def pour_metal(self, mode='normal'):
		self._filled_lvl = min(self._height, self._filled_lvl + self._filling_rate)
		# just start filling link again when playing in infinite mode
		if mode == 'infinite':
			if self._filled_lvl == self._height:
				self._filled_lvl = self._filling_rate

	def update(self):
		""" If Link is filled than it should go into challenge proposal stage
		if it is in challenge proposal state then see if it is expired already
		Once link is done, it should create corresponding event"""
		if self._stage == LinkStage.FILLING:
			if self._filled_lvl == self._height:
				self.refresh_clock()
				self._stage = LinkStage.CHALLENGE_PROPOSAL
		elif self._stage == LinkStage.CHALLENGE_PROPOSAL:
			self.update_ttl()
			if not self.is_still_alive():
				# fixme useful flag?
				if not self._event_posted:
					pygame.event.post(LINK_METAL_EVENT_DICT[self._metal])
					self._event_posted = True
				self._stage = LinkStage.DONE
