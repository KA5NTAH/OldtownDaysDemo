from abc import ABC, abstractmethod
from game_enums.user_intention import UserIntention


class ResponsiveObject(ABC):
    """
    Responsive object keeps track of specific user's action directed at this class.
    That means class can read user action and understand if it was addressed or not.
    At every moment of time ResponsiveObject can tell if this action was done or not.
    Given two consecutive user's action Object can identify user's intention
    """
    def __init__(self, *args):
        self.last_directed_action = self._get_directed_action()

    def get_user_intention_and_update_track(self) -> UserIntention:
        """based on two consecutive actions identify user intention then update last action with current"""
        curr_action = self._get_directed_action()
        result_intention = UserIntention.IGNORE
        if curr_action and not self.last_directed_action:
            result_intention = UserIntention.SWITCH_ON
        elif curr_action and self.last_directed_action:
            result_intention = UserIntention.KEEP_ON_STATE
        elif not curr_action and self.last_directed_action:
            result_intention = UserIntention.SWITCH_OFF
        self.last_directed_action = curr_action
        return result_intention

    def _get_directed_action(self):
        """get action with respect to object being addressed"""
        if not self._is_addressed():
            return False
        return self._get_user_action()

    @abstractmethod
    def _get_user_action(self) -> bool:
        """get state of the action that object is bound to track"""

    @abstractmethod
    def _is_addressed(self) -> bool:
        """tells if user's action is directed at this object or not"""
