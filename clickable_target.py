from abc import ABC, abstractmethod
from game_enums.target_pressing_state import TargetPressingState


class ClickableTarget:
    def __init__(self):
        self._old_user_action = self._get_user_action()

    def get_pressed_cond(self) -> TargetPressingState:
        curr_user_action = self._get_user_action()
        if curr_user_action and not self._old_user_action:
            return TargetPressingState.GOT_PRESSED
        elif curr_user_action and self._old_user_action:
            return TargetPressingState.LONG_TIME_PRESSED
        elif not curr_user_action and self._old_user_action:
            return TargetPressingState.GOT_RELEASED
        elif not curr_user_action and not self._old_user_action:
            return TargetPressingState.NOT_PRESSED

    def update_user_action(self):
        self._old_user_action = self._get_user_action()

    @abstractmethod
    def _get_user_action(self) -> bool:
        pass

    @abstractmethod
    def _is_mouse_inside(self) -> bool:
        pass
