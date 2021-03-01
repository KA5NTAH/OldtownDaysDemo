import pygame
import sys
from enum import Enum, auto

size = (1000, 800)
screen = pygame.display.set_mode(size)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Condition(Enum):
    STANDARD_PLAY = auto()
    CHALLENGE_WAITING = auto()
    CHALLENGE = auto()


clock = pygame.time.Clock()
curr_state = Condition.CHALLENGE_WAITING
time_to_accept_challenge = 1 * 1000
challenge_time = 1 * 1000
challenge_line_length = 900
waiting_line_length = 900
time_spent_in_challenge = 0
time_spent_in_waiting = 0
old_space = pygame.key.get_pressed()[pygame.K_SPACE]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # ========================= mouse handler

    screen.fill(black)
    # update
    if curr_state == Condition.STANDARD_PLAY:
        time_spent_in_challenge = 0
        time_spent_in_waiting = 0
    if curr_state == Condition.CHALLENGE_WAITING:
        time_spent_in_challenge = 0
        time_spent_in_waiting += clock.tick()
        if time_spent_in_waiting >= time_to_accept_challenge:
            curr_state = Condition.STANDARD_PLAY
        curr_space = pygame.key.get_pressed()[pygame.K_SPACE]
        if curr_space and not old_space:
            old_space = curr_space
            curr_state = Condition.CHALLENGE
        old_space = curr_space
    if curr_state == Condition.CHALLENGE:
        time_spent_in_waiting = 0
        time_spent_in_challenge += clock.tick()
        if time_spent_in_challenge >= challenge_time:
            curr_state = Condition.STANDARD_PLAY

    # draw
    if curr_state == Condition.STANDARD_PLAY:
        screen.fill(green)
    if curr_state == Condition.CHALLENGE_WAITING:
        screen.fill(blue)
        spent_length = waiting_line_length * (time_spent_in_waiting / time_to_accept_challenge)
        line_len = waiting_line_length - spent_length
        pygame.draw.line(screen, (255, 0, 0), (50, 400), (50 + int(line_len), 400), 5)
    if curr_state == Condition.CHALLENGE:
        spent_length = challenge_line_length * (time_spent_in_challenge / challenge_time)
        line_len = challenge_line_length - spent_length
        pygame.draw.line(screen, (255, 0, 0), (50, 400), (50 + int(line_len), 400), 5)

    pygame.display.flip()
