class ProgressBar:
    def __init__(self, bg_img, empty_part, filled_part, vertical_orientation: bool, inner_part_offset: tuple,
                 pos: tuple, limit: int):
        self._bg_img = bg_img
        self._empty_part_img = empty_part
        self._filled_part_img = filled_part
        self._vertical_orientation = vertical_orientation
        self._inner_part_offset = inner_part_offset
        self._position = pos
        self._progress = 0
        _, _, self._inner_w, self._inner_h = self._empty_part_img.get_rect()
        self._limit = limit
        self._inner_part_pos = (self._position[0] + self._inner_part_offset[0],
                                self._position[1] + self._inner_part_offset[1])
        if self._vertical_orientation:
            self._filling_rate = self._inner_h / limit
        else:
            self._filling_rate = self._inner_w / limit

    def increment_progress(self):
        self._progress = min(self._progress + 1, self._limit)

    def draw(self, screen):
        screen.blit(self._bg_img, self._position)
        if self._vertical_orientation:
            """
            A ----- *
            |       |
            C ----- B
            |*******|
            * ----- D
            """
            inner_part_bottom_y = self._inner_part_pos[1] + self._inner_h
            filled_part = self._filling_rate * self._progress
            surface_y = inner_part_bottom_y - filled_part
            surface_y = int(surface_y)
            A = (0, 0)
            B = (self._inner_w, self._inner_h - filled_part)
            C = (0, self._inner_h - filled_part)
            D = (self._inner_w, self._inner_h)
            screen.blit(self._empty_part_img, self._inner_part_pos, (*A, *B))
            screen.blit(self._filled_part_img, (self._inner_part_pos[0], surface_y), (*C, *D))
        else:
            """
            A -------- C ------- *
            |**********|         | 
            * -------- B --------D
            """
            filled_part = self._filling_rate * self._progress
            surface_x = self._inner_part_pos[0] + filled_part
            A = (0, 0)
            B = (filled_part, self._inner_h)
            C = (filled_part, 0)
            D = (self._inner_w, self._inner_h)
            screen.blit(self._empty_part_img, (self._inner_part_pos[0] + filled_part, self._inner_part_pos[1]), (*C, *D))
            screen.blit(self._filled_part_img, self._inner_part_pos, (*A, *B))

    def nullify_progress(self):
        self._progress = 0
