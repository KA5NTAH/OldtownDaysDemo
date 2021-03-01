import pygame
from challenge_target import ChallengeTarget
from collections import deque
import numpy as np
import sys

pygame.font.init()


GOLD = (255, 215, 0)


class Challenge:
    def __init__(self, target_list):
        self.targets = target_list
        self.target_number = len(self.targets)
        self.ixs_permutations = np.random.permutation(self.target_number)
        self.ixs_dict = dict(zip(self.ixs_permutations[::-1], np.arange(self.target_number) + 1))
        self.challenge_order = deque(self.ixs_permutations)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.curr_ind = self.challenge_order.pop()

    def draw(self, screen):
        for i in range(self.target_number):
            if i in self.challenge_order or i == self.curr_ind:
                text_number = f'{self.ixs_dict[i]}'
                # todo number should be part of challenge target
                text_surface = self.font.render(text_number, False, (153, 0, 0))
                self.targets[i].draw(screen)
                screen.blit(text_surface, (self.targets[i].cx, self.targets[i].cy))

    def update(self):
        for i in range(self.target_number):
            self.targets[i].update()
            if self.targets[i].can_be_activated() and i == self.curr_ind and self.challenge_order:
                self.curr_ind = self.challenge_order.pop()
        # todo check if deque is empty and return some state?
        if not self.challenge_order:
            print(f'CHALLENGE IS DONE')


if __name__ == '__main__':
    screen = pygame.display.set_mode((1000, 800))
    target = ChallengeTarget(5000, 150, 150, GOLD)
    target1 = ChallengeTarget(5000, 600, 600, GOLD)
    target2 = ChallengeTarget(5000, 600, 150, GOLD)
    target3 = ChallengeTarget(5000, 400, 400, GOLD)
    target4 = ChallengeTarget(5000, 150, 600, GOLD)
    challenge = Challenge([target, target1, target2, target3, target4])
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((255, 255, 255))
        # update block
        challenge.update()
        # draw block
        challenge.draw(screen)
        pygame.display.flip()
