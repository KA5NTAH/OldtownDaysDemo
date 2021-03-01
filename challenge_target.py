from expiringtarget import ExpiringTarget
import pygame
import sys


GOLD = (255, 215, 0)
BLEAK = (15, 15, 15)


class ChallengeTarget(ExpiringTarget):
    def __init__(self, time, cx, y, color):
        super().__init__(time)
        self.radius = 30
        self.cx = cx
        self.cy = y
        self.color = color
        # left, top, width, height
        self.rect = pygame.Rect(int(self.cx - self.radius),
                                int(self.cy - self.radius),
                                self.radius * 2,
                                self.radius * 2)
        self.old_mouse, _, _ = pygame.mouse.get_pressed()

    def can_be_activated(self):
        curr_mouse, _, _ = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        diff_from_center = ((self.cx - mx) ** 2 + (self.cy - my) ** 2) ** 0.5
        mouse_is_inside = diff_from_center <= self.radius
        clicked = curr_mouse and not self.old_mouse
        self.old_mouse = curr_mouse
        return clicked and mouse_is_inside

    def is_expired(self):
        return self.ttl == 0

    def update(self):
        self.update_ttl()

    def draw(self, screen):
        pygame.draw.circle(screen, GOLD, (self.cx, self.cy), self.radius)
        # draw unfilled area
        unfilled_height = int((self.ttl / self.time) * self.rect.height)
        unfilled_clip = pygame.Rect((self.rect.left,
                                     self.rect.top,
                                     self.rect.width,
                                     unfilled_height))
        screen.set_clip(unfilled_clip)
        pygame.draw.circle(screen, BLEAK, (self.cx, self.cy), self.radius)
        screen.set_clip(None)

        # draw filled area
        filled_height = self.rect.height - unfilled_height
        filled_clip = pygame.Rect((self.rect.left,
                                   self.rect.top + unfilled_height,
                                   self.rect.width,
                                   filled_height))
        screen.set_clip(filled_clip)
        pygame.draw.circle(screen, self.color, (self.cx, self.cy), self.radius)
        screen.set_clip(None)


if __name__ == '__main__':
    screen = pygame.display.set_mode((1000, 800))
    target = ChallengeTarget(5000, 400, 500, GOLD)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((255, 255, 255))
        # update block
        target.update()
        # draw block
        target.draw(screen)
        pygame.display.flip()
