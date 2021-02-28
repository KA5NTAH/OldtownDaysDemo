import pygame
import utils
import sys
from link import Link
from ball import Ball


class Channel:
	def __init__(self, link_metal_key, boundaries, filling_rate=None):
		self.rect = boundaries
		self.balls = []
		self.ball_cx = self._init_ball_cx()
		# should be used only while init
		self.link, self.link_place = self._init_link(link_metal_key, filling_rate)
		# link_is_free means free to recieve ball
		self.link_is_open = True
		self.swap_thrd = 0.5
		self.recieve_ball_thrd = 50
		self.discarded_balls = 0

		# ball fate consts
		self.BALL_KEEP_MOVE = "move"
		self.DISCARD_BALL = "discard"
		self.FILL_LINK_WITH_BALL = "fill"

	def _init_link(self, link_metal_key, filling_rate=None):
		left, top, w, h, = self.rect
		# resize img that link rectangle w fits channel w
		# todo keep metal_keys as consts in some file
		empty_img, filled_img = utils.load_images_by_metal_key(link_metal_key)
		_, _, link_w, link_h = filled_img.get_rect()
		scale = w / link_w
		link_w *= scale
		link_h *= scale
		link_w, link_h = int(link_w), int(link_h)
		filled_img = pygame.transform.scale(filled_img, (link_w, link_h))
		empty_img = pygame.transform.scale(empty_img, (link_w, link_h))

		# link should be at the bottom of the chanel (load link as the one method)
		link_start_pos = (left, top + h - link_h)
		link = Link(link_start_pos, empty_img, filled_img, link_metal_key)
		if filling_rate is not None:
			link.set_fill_rate(filling_rate)
		link_place = pygame.Rect(*link_start_pos, link_w, link_h)
		return link, link_place

	def _init_ball_cx(self):
		left, top, w, h = self.rect
		cx = int(left + w / 2)
		return cx

	def set_ball(self, ball):
		# count ball position
		l, t, w, h = ball._rect  # todo write getter for ball rectangle
		ball_top = self.rect.top
		ball_left = int(self.ball_cx - w / 2)
		ball.place_ball_at_pos((ball_left, ball_top))
		self.balls += [ball]

	def yield_link(self):
		if self.link_is_open:
			self.link_is_open = False
			return self.link

	def swap_manager(self, channel, link):
		# swap is handled from reciever position
		swapped = False
		links_iou = utils.get_iou(link.rect, self.link_place)
		if links_iou > self.swap_thrd and self.link_is_open:
			give_away_link = self.yield_link()
			channel.replace_link(give_away_link)
			self.replace_link(link)
			swapped = True
		return swapped

	def replace_link(self, link):
		self.link = link
		self.link.rect = self.link_place
		self.link_is_open = True

	# todo write logic
	def update(self):
		# move balls
		# handle collisions
		balls_ixs_to_keep = []
		for b_ind, ball in enumerate(self.balls):
			ball.fall()
			fate = self.get_ball_fate(ball)
			# get balls intersections
			if fate == self.FILL_LINK_WITH_BALL:
				self.link.fill()
			elif fate == self.BALL_KEEP_MOVE:
				balls_ixs_to_keep += [b_ind]
			elif fate == self.DISCARD_BALL:
				self.discarded_balls += 1
		self.balls = [b for ind, b in enumerate(self.balls) if ind in balls_ixs_to_keep]

	def get_ball_fate(self, ball):
		# some kind of enumerate
		# fate is either : KEEP_MOVING, DISCARD, FILL_LINK
		intersection = utils.get_intersection(ball._rect, self.link.rect)
		if intersection < self.recieve_ball_thrd:
			return self.BALL_KEEP_MOVE
		same_metal = self.link.check_metal_compatibility(ball)
		if same_metal and self.link_is_open and not self.link.is_filled():
			return self.FILL_LINK_WITH_BALL
		return self.DISCARD_BALL

	def draw(self, screen):
		for ball in self.balls:
			ball.draw(screen)
		self.link.draw(screen)

	def link_spot_is_touched(self, mouse_pos):
		if not self.link_is_open:
			return False
		# i think this must be in utils
		x, y = mouse_pos
		left, top, w, h = self.link_place
		return left <= x <= left + w and top <= y <= top + h


if __name__ == "__main__":
	import random as rd
	size = (1000, 800)
	screen = pygame.display.set_mode(size)
	rect1 = pygame.Rect(100, 0, 200, 700)
	rect2 = pygame.Rect(350, 0, 200, 700)
	gold_channel = Channel(utils.GOLDEN_COLOR, rect1)
	black_iron_channel = Channel(utils.BLACK_IRON_COLOR, rect2)

	ball_speed = (0, 2)
	ball = Ball(utils.GOLDEN_COLOR, ball_speed)
	gold_channel.set_ball(ball)

	SET_BALL = pygame.USEREVENT + 1
	pygame.time.set_timer(SET_BALL, 1000)
	channels = [gold_channel, black_iron_channel]
	colors = [utils.GOLDEN_COLOR, utils.BLACK_IRON_COLOR]

	old_button_state, _, _ = pygame.mouse.get_pressed()
	controlled_link = None
	robbed_channel_ind = None
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == SET_BALL:
				color = rd.choice(colors)
				ball = Ball(color, ball_speed)
				chan_ix = rd.randrange(len(channels))
				channels[chan_ix].set_ball(ball)

		# ================================================================= mouse handler
		button, _, _ = pygame.mouse.get_pressed()
		rel = pygame.mouse.get_rel()
		if button and not old_button_state:
			print(f'FIRST  PRESS')
			pos = pygame.mouse.get_pos()
			for c_ind, chanel in enumerate(channels):
				if chanel.link_spot_is_touched(pos):
					print("TOUCHED")
					link = chanel.yield_link()
					if link is not None:
						print("CONTROLLED")
						controlled_link = link
						robbed_channel_ind = c_ind
						break
					else:
						controlled_link = None

		elif button and old_button_state:
			if controlled_link is not None:
				controlled_link.move((rel[0], 0))
				# print(f'rel = {rel}')
			pass
		elif old_button_state and not button:
			# release from button
			# swap manager
			print("RELEASE")
			if controlled_link is not None:
				for channel in channels:
					swapped = channel.swap_manager(channels[robbed_channel_ind], controlled_link)
					if swapped:
						break
				else:
					channels[robbed_channel_ind].replace_link(controlled_link)

			robbed_channel_ind = None
			controlled_link = None
		old_button_state = button
		# ================================================================= mouse handler

		discarded = 0
		for channel in channels:
			discarded += channel.discarded_balls
		# print(f'DISCARDED = {discarded}')

		screen.fill((255, 255, 255))
		for channel in channels:
			channel.update()
			channel.draw(screen)
		if controlled_link is not None:
			controlled_link.draw(screen)
		pygame.display.flip()
