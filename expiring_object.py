import pygame


class ExpiringObject:
    def __init__(self, life_time):
        self._life_time = life_time
        self._clock = pygame.time.Clock()
        self._ttl = self._life_time

    def refresh_clock(self):
        self._clock.tick()

    def update_ttl(self) -> None:
        self._ttl -= self._clock.tick()
        self._ttl = max(0, self._ttl)

    def is_still_alive(self) -> bool:
        return self._ttl > 0


a = ExpiringObject(5)
a.update_ttl()
