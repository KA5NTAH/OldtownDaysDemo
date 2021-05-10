import pygame
import utils
import sys
from link import Link
from droplet import Droplet
import game_constants
import os
from game_enums.metals import Metals
from game_enums.link_stage import LinkStage
import game_constants
pygame.init()


# todo add doc string
class Channel:
	def __init__(self, link):
		self._link = link
		self._link_rect = pygame.Rect(*link.addressing_rect)  # todo rename
		self._droplets = []
		self.channel_rect = pygame.Rect(*self._link.addressing_rect)
		self.channel_rect.top = 0

	@property
	def link_rect(self):
		return self._link_rect

	@property
	def link_stage(self):
		return self._link.stage

	@property
	def link_metal(self):
		return self._link.metal

	def refresh_link(self):
		self._link.refresh_clock()

	def get_and_update_link_intention(self):
		return self._link.get_user_intention_and_update_track()

	# fixme pass speed of drop as argument or define it in game constant
	def create_and_set_ball(self, metal):
		half_width = int(self.channel_rect.width / 2)
		drop_x = self.channel_rect.left + half_width - int(game_constants.DROPLET_WIDTH / 2)
		drop_y = self.channel_rect.top
		drop = Droplet(metal, 2, (drop_x, drop_y))
		self._droplets.append(drop)

	def link_is_available(self):
		return self._link is not None

	def update(self):
		""" All droplets fall
		Then if droplet is in the place where link should be there is three possible outcomes
		1) There is link, and droplet is of the same metal - success
		2) There is link, and droplet is of the different metal - droplet is ruined
		3) There is no link - ambiguous situation (for example it is not ruined if respective link is already filled)
		Impossible to decide using channel info only -> sent event
		In either way that means droplet doesnt need to be updated anymore/when droplet is ruined method tells
		about it through event"""
		droplets_ixs_to_discard = []
		for index in range(len(self._droplets)):
			self._droplets[index].fall()
			intersection = utils.get_intersection(self._link_rect, self._droplets[index].rect)
			if intersection > game_constants.DROPLET_LINK_INTERSECTION_THRD:
				droplets_ixs_to_discard.append(index)
				if self._link is None:
					ruined_metal = self._droplets[index].metal
					pygame.event.post(game_constants.NO_LINK_RUIN_DICT[ruined_metal])
				else:
					if self._link.metal == self._droplets[index].metal:
						self._link.pour_metal()
					else:
						pygame.event.post(game_constants.RUINED_DROP_EVENT)
		# keep only ones that still move
		self._droplets = [self._droplets[i] for i in range(len(self._droplets)) if i not in droplets_ixs_to_discard]
		if self._link is not None:
			self._link.update()
			if self._link.stage == LinkStage.DONE:
				self._link = None

	def draw(self, screen):
		for drop in self._droplets:
			drop.draw(screen)
		if self._link is not None:
			self._link.draw(screen)
		else:
			screen.blit(game_constants.EMPTY_LINK_FILLER, self._link_rect)

	def yield_link(self):
		link = self._link
		self._link = None
		return link

	def set_link(self, link):
		self._link = link
		if self._link is not None:
			self._link.addressing_rect = self._link_rect


if __name__ == '__main__':
	pygame.init()
	from game_constants import LINKS_DIR
	# empty , full, timer, position, time, metal
	m = Metals.GOLD
	gpath = os.path.join(LINKS_DIR, m.name)
	empty = pygame.image.load(os.path.join(gpath, 'Empty.png'))
	full = pygame.image.load(os.path.join(gpath, 'Full.png'))
	timer = pygame.image.load(os.path.join(gpath, 'FullTimer.png'))
	link = Link(empty, full, timer, (40, 533), 5000, Metals.GOLD, game_constants.MOUSE_KEY)
	p = Channel(link)
	width, height = 1200, 680
	black = (255, 255, 255)
	size = (width, height)
	screen = pygame.display.set_mode(size)

	ttl = 1500
	clock = pygame.time.Clock()
	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				sys.exit()
		screen.fill(black)
		ttl -= clock.tick()
		if ttl < 0:
			p.create_and_set_ball(Metals.GOLD)
			ttl = 100
		p.update()
		p.draw(screen)
		pygame.display.flip()
