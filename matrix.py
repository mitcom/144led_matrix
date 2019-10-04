import time

from ansi import Terminal


BLACK = 0, 0, 0
WHITE = 255, 255, 255


class Matrix():
    pixel = '███'

    def __init__(self, size_x, size_y, auto_show=False, fill=BLACK):
        self.size_x = size_x
        self.size_y = size_y

        self.__create_matrix()

        terminal = Terminal()
        terminal.safe_prepare()
        self.terminal = terminal

        self._auto_show = auto_show

        self.fill(fill)

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

    def _showable(method):
        def method_wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            if self._auto_show:
                self.show()
            return result

        return method_wrapper

    @_showable
    def fill(self, color):
        for y in self.rows:
            for x in self.cells:
                self._matrix[x][y] = color

    @_showable
    def set_pixel(self, x, y, color):
        self._matrix[x][y] = color

    @_showable
    def set_pixels(self, pixels):
        for y, rows in enumerate(pixels):
            if y < self.size_y:
                for x, pixel in enumerate(rows):
                    if x < self.size_x:
                        self._matrix[x][y] = pixel

    @_showable
    def set_BW_pixels(self, pixels):
        for y, rows in enumerate(pixels):
            if y < self.size_y:
                for x, pixel in enumerate(rows):
                    if x < self.size_x:
                        self._matrix[x][y] = WHITE if pixel else BLACK

    def show(self):
        self.terminal.go_to_origin()
        for y in self.rows:
            self.print_line(y)

    def print_line(self, line):
        with self.terminal.line:
            for x in self.cells:
                self.terminal.write(self.pixel, self._matrix[x][line])


class MatrixWithGaps(Matrix):
    pixel = '▆▆ '


class MatrixLargerPixelsWithGaps(Matrix):
    upper_pixel = '▄▄▄ '
    lower_pixel = '███ '

    def print_line(self, line):
        with self.terminal.line:
            for x in self.cells:
                self.terminal.write(self.upper_pixel, self._matrix[x][line])
        with self.terminal.line:
            for x in self.cells:
                self.terminal.write(self.lower_pixel, self._matrix[x][line])


class MatrixSmallPixelsWithGaps(Matrix):
    pixel = '▄ '

    def print_line(self, line):
        with self.terminal.line:
            for x in self.cells:
                self.terminal.write(self.pixel, self._matrix[x][line])


class MatrixBigPixelsWithGaps(Matrix):
    pixel = '████  '

    def print_line(self, line):
        t = self.terminal
        with t.line:
            for x in self.cells:
                t.write(self.pixel, self._matrix[x][line])
        with t.line:
            for x in self.cells:
                t.write(self.pixel, self._matrix[x][line])
        self.terminal.break_line()


class MatrixBigPixels(Matrix):
    pixel = '████'

    def print_line(self, line):
        t = self.terminal
        with t.line:
            for x in self.cells:
                t.write(self.pixel, self._matrix[x][line])
        with t.line:
            for x in self.cells:
                t.write(self.pixel, self._matrix[x][line])

def partition(chunks):
    if chunks == 0:
        return

    step = 1 / chunks
    value = step
    while value < 1.0:
        yield value
        value += step

def mul(factor, iterable):
    return [min(factor -1, ceil(factor * i)) for i in iterable]

def modify_hue(hue, hls):
    h, l, s = hls
    return hue, l, s

def symmetric_range(steps):
    def f(x):
        return x*x

    def normalize(sequence, min_r, max_r):
        max_x = sequence[-1]
        min_x = sequence[0]
        diff = max_x - min_x

        values = [(x - min_x)/diff for x in sequence]

        diff_r = max_r - min_r
        return [(v * diff_r) + min_r for v in values]

    values = [
        f(i) for i in range(steps)
    ]
    values = normalize(values, 0.35, 0.9)

    return values + values[::-1]


from math import ceil
from itertools import cycle
from random import randint
import colorsys
# RED = 61/256,164/256,171/256
RED = 1,0,0
# red_hls = colorsys.rgb_to_hls(*RED)

def next_value(index, values):
    next_index = (index + 1) % len(values)
    return next_index, values[next_index]

if __name__ == '__main__':
    PIGMENTS = 600
    BRIGHTNESS = 30

    Y = 12
    X = 12

    m = MatrixSmallPixelsWithGaps(X, Y, auto_show=False, fill=BLACK)

    _ = False
    O = True

    shape = [
        [_, _, _, _, _, O, O, _, _, _, _, _],
        [_, _, _, _, O, O, O, O, _, _, _, _],
        [_, _, _, _, _, O, O, _, _, _, _, _],
        [_, _, _, _, O, O, O, O, _, _, _, _],
        [_, _, _, O, O, O, O, O, O, _, _, _],
        [_, _, _, _, O, O, O, O, _, _, _, _],
        [_, _, _, O, O, O, O, O, O, _, _, _],
        [_, _, O, O, O, O, O, O, O, O, _, _],
        [_, _, _, O, O, O, O, O, O, _, _, _],
        [_, _, O, O, O, O, O, O, O, O, _, _],
        [_, O, O, O, O, O, O, O, O, O, O, _],
        [_, _, _, _, O, O, O, O, _, _, _, _],
    ]

    data_matrix = [
        [
            [
                randint(0, PIGMENTS-1) if shape[y][x] else None,
                randint(0, 2 * BRIGHTNESS) if shape[y][x] else None,
            ]
            for x in range(X)
        ] for y in range(Y)
    ]

    colors = list(partition(PIGMENTS))
    lightnesses = symmetric_range(BRIGHTNESS)

    while(True):

        for y in m.rows:
            for x in m.cells:
                if shape[y][x]:
                    h_index, l_index = data_matrix[y][x]
                    h_index, hue = next_value(h_index, colors)
                    l_index, lightness = next_value(l_index, lightnesses)

                    data_matrix[y][x] = h_index, l_index

                    rgb = mul(256, colorsys.hls_to_rgb(hue, lightness, 0.5))
                    m.set_pixel(x, y, rgb)
        m.show()
        time.sleep(0.1)
