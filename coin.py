from responsive_objects.mouse_responsive import MouseResponsive
from responsive_objects.circle_responsive import CircleResponsive
from game_enums.coins_kinds import CoinsKinds
from expiring_object import ExpiringObject
from game_constants import COINS_IMAGES, COINS_RADIUS
import pygame
from math import pi


class Coin(CircleResponsive, MouseResponsive, ExpiringObject):
    """Coin is object that can be clicked on and which life time os represented by arc around it"""
    def __init__(self, coin_kind, cx, cy, mouse_key, time):
        super().__init__(cx, cy, COINS_RADIUS, mouse_key)
        self._coin_kind = coin_kind
        offset = 3
        self._arc_rect = pygame.Rect(self._cx - self._radius - offset,
                                     self._cy - self._radius - offset,
                                     self._radius * 2 + offset * 2,
                                     self._radius * 2 + offset * 2)
        self._image = COINS_IMAGES[coin_kind]
        ExpiringObject.__init__(self, time)

    @property
    def coin_kind(self):
        return self._coin_kind

    def draw(self, screen):
        if self.is_still_alive():
            """Main purpose of coin is to draw arc around image representing time passed"""
            color = (255, 215, 0)  # todo set in game constants
            start_angle = pi / 2
            # todo fix animation maybe convert image from pill
            stop_angle = start_angle + 2 * pi * (self._ttl / self._life_time)
            pygame.draw.ellipse(screen, (0, 0, 0), self._arc_rect, 0)
            pygame.draw.arc(screen, color, self._arc_rect, start_angle, stop_angle, width=20)
            screen.blit(self._image, (self._cx - self._radius, self._cy - self._radius))


if __name__ == "__main__":
    pygame.init()
    import sys
    time = 10 * 1000
    coin = Coin(CoinsKinds.FAITH_COIN, 500, 200, 0, time)
    coin1 = Coin(CoinsKinds.BLACKFYRE_COIN, 200, 200, 0, time)
    coin2 = Coin(CoinsKinds.TARGARYEN_COIN, 900, 200, 0, time)
    screen = pygame.display.set_mode((1200, 680))
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((0, 255, 0))
        coin.update_ttl()
        coin1.update_ttl()
        coin2.update_ttl()
        coin.draw(screen)
        coin1.draw(screen)
        coin2.draw(screen)
        pygame.display.flip()
