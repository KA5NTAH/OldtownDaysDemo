from responsive_objects.responsive import ResponsiveObject


class Slide(ResponsiveObject):
    def __init__(self, *args):
        """Slide is responsive object that is always adressed"""
        super().__init__(*args)

    def _is_addressed(self) -> bool:
        return True
