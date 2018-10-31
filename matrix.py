import time

import ansi


BLACK = 0,0,0
WHITE = 255, 255, 255

PIXEL = '▄ '


class Matrix():
    def __init__(self, size_x, size_y, auto_show=False):
        self.size_x = size_x
        self.size_y = size_y

        self.__create_matrix()

        # this is used for returning to position 0, 0 before drawing every
        # (without first) frame
        self._after_first_frame = False

        self._auto_show = auto_show

        self.fill((0,0,0))

    def __create_matrix(self):
        self._matrix = [
            [BLACK] * self.size_y for x in self.__cells()
        ]

    def __rows(self):
        return range(self.size_y)

    def __cells(self):
        return range(self.size_x)

    def fill(self, color):
        for y in self.__rows():
                for x in self.__cells():
                    self._matrix[x][y] = color

        if self._auto_show:
            self.show()

    def set_pixel(self, x, y, color):
        self._matrix[x][y] = color

        if self._auto_show:
            self.show()

    def show(self):
        if self._after_first_frame:
            ansi.move_cursor_up(self.size_y + 1)
        else:
            self._after_first_frame = True

        with ansi.terminal():
            for y in self.__rows():
                for x in range (self.size_x):
                    ansi.write(PIXEL, self._matrix[x][y])
                ansi.write()


if __name__ == '__main__':
    size_x = 4
    size_y = 3
    m = Matrix(size_x, size_y, auto_show=True)
    for y in range(size_y):
        for x in range(size_x):
            m.set_pixel(x, y, WHITE)
            time.sleep(0.05)
