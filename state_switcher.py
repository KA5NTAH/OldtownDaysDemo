from responsive_objects.button import Button
from game_enums.user_intention import UserIntention
from typing import List


class StateSwitcher:
    def __init__(self, buttons: List[Button], states, background_image=None):
        """
        State switcher is container for buttons and states corresponding to them When button is pressed class
        returns respective state
        """
        self._buttons = buttons
        self._states = states
        self._bg_img = background_image

    def update_and_returned_selected_state(self):
        user_intentions = [self._buttons[i].get_user_intention_and_update_track() for i in range(len(self._buttons))]
        for index, intention in enumerate(user_intentions):
            if intention == UserIntention.SWITCH_ON:
                return self._states[index]
        return None

    def draw(self, screen):
        if self._bg_img is not None:
            screen.blit(self._bg_img)
        for b in self._buttons:
            b.draw(screen)
