from clickable_target import ClickableTarget
from game_enums.target_pressing_state import TargetPressingState
import pygame


class ExpiringClickableTarget(ClickableTarget):
    def __init__(self, life_time):
        super().__init__()
        self._life_time = life_time
        self._clock = pygame.time.Clock
        self._ttl = self._life_time

    def update_ttl(self) -> None:
        self._ttl -= self.clock.tick()
        self._ttl = max(0, self.ttl)

    def is_still_alive(self) -> bool:
        return self._ttl > 0

    def can_be_activated(self) -> bool:
        press_state = self.get_pressed_cond()
        return press_state == TargetPressingState.GOT_PRESSED and self._is_mouse_inside()
