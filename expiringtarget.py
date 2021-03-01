import pygame
from abc import ABC, abstractmethod


class ExpiringTarget:
    def __init__(self, time):
        self.time = time
        self.ttl = time
        self.clock = pygame.time.Clock()

    @abstractmethod
    def can_be_activated(self):
        pass

    @abstractmethod
    def is_expired(self):
        pass

    def update_ttl(self):
        self.ttl -= self.clock.tick()
        self.ttl = max(0, self.ttl)

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

