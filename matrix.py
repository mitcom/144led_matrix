import time

from ansi import Terminal


BLACK = 0,0,0
WHITE = 255, 255, 255

PIXEL = '▄ '


class Matrix():
    def __init__(self, size_x, size_y, auto_show=False):
        self.size_x = size_x
        self.size_y = size_y

        self.__create_matrix()

        terminal = Terminal()
        terminal.safe_prepare()
        self.terminal = terminal

        self._auto_show = auto_show

        self.fill((0,0,0))

    def __create_matrix(self):
        self._matrix = [
            [BLACK] * self.size_y for x in self.cells
        ]

    @property
    def rows(self):
        return range(self.size_y)

    @property
    def cells(self):
        return range(self.size_x)

    def _auto_showable(method):
        def method_wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            if self._auto_show:
                self.show()
            return result

        return method_wrapper

    @_auto_showable
    def fill(self, color):
        for y in self.rows:
            for x in self.cells:
                self._matrix[x][y] = color

    @_auto_showable
    def set_pixel(self, x, y, color):
        self._matrix[x][y] = color

    def show(self):
        self.terminal.go_to_origin()
        for y in self.rows:
            with self.terminal.line:
                for x in self.cells:
                    self.terminal.write(PIXEL, self._matrix[x][y])


if __name__ == '__main__':
    m = Matrix(4, 4, auto_show=True)
    for y in m.rows:
        for x in m.cells:
            m.set_pixel(x, y, WHITE)
            time.sleep(0.05)
