import pygame
import sys
import utils


class Ball:
    def __init__(self, metal_key, speed):
        self._metal_key = metal_key
        self._speed = speed
        # self._img = img  # todo might be we could use some animation
        # todo set constant just for now
        self._rect = pygame.Rect(0, 0, 50, 50)

    def place_ball_at_pos(self, position):
        left, top = position
        self._rect.left = left
        self._rect.top = top

    def fall(self):
        self._rect = self._rect.move(self._speed)

    def draw(self, screen):
        color = 0
        # circle(surface, color, center, radius) -> Rect
        if self._metal_key == utils.GOLDEN_COLOR:
            color = (255, 215, 0)
        elif self._metal_key == utils.BLACK_IRON_COLOR:
            color = (59, 61, 63)
        l, t, w, h = self._rect
        raduis = int(w / 2)
        center = (int(l + w/ 2), int(t + h/ 2))
        pygame.draw.circle(screen, color, center, raduis)


if __name__ == "__main__":
    size = width, height = 1000, 800
    screen = pygame.display.set_mode(size)
    ball = Ball(utils.GOLDEN_COLOR, (0, 1))

    SET_BALL = pygame.USEREVENT + 1
    pygame.time.set_timer(SET_BALL, time)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((255, 255, 255))
        ball.fall()
        ball.draw(screen)
        pygame.display.flip()

