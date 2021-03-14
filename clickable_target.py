from abc import ABC, abstractmethod
from game_enums.user_intention import UserIntention


class ClickableTarget:
    def __init__(self):
        self._old_user_action = self._get_user_action()

    def get_pressed_cond(self) -> UserIntention:
        curr_user_action = self._get_user_action()
        if curr_user_action and not self._old_user_action:
            return UserIntention.SWITCH_ON
        elif curr_user_action and self._old_user_action:
            return UserIntention.KEEP_ON_STATE
        elif not curr_user_action and self._old_user_action:
            return UserIntention.SWITCH_OFF
        elif not curr_user_action and not self._old_user_action:
            return UserIntention.IGNORE

    def update_user_action(self):
        self._old_user_action = self._get_user_action()

    @abstractmethod
    def _get_user_action(self) -> bool:
        pass

    @abstractmethod
    def _is_mouse_inside(self) -> bool:
        pass
