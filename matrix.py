import time

from ansi import Terminal


BLACK = 0, 0, 0
WHITE = 255, 255, 255


class Matrix:
    pixel = "███"

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
        self._matrix = [[BLACK] * self.size_y for x in self.cells]

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

    def show(self):
        self.terminal.go_to_origin()
        for y in self.rows:
            self.print_line(y)

    def print_line(self, line):
        with self.terminal.line:
            for x in self.cells:
                self.terminal.write(self.pixel, self._matrix[x][line])


class MatrixWithGaps(Matrix):
    pixel = "▆▆ "


class MatrixLargerPixelsWithGaps(Matrix):
    upper_pixel = "▄▄▄ "
    lower_pixel = "███ "

    def print_line(self, line):
        with self.terminal.line:
            for x in self.cells:
                self.terminal.write(self.upper_pixel, self._matrix[x][line])
        with self.terminal.line:
            for x in self.cells:
                self.terminal.write(self.lower_pixel, self._matrix[x][line])


class MatrixSmallPixelsWithGaps(Matrix):
    pixel = "▄ "

    def print_line(self, line):
        with self.terminal.line:
            for x in self.cells:
                self.terminal.write(self.pixel, self._matrix[x][line])


class MatrixBigPixelsWithGaps(Matrix):
    pixel = "████  "

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
    pixel = "████"

    def print_line(self, line):
        t = self.terminal
        with t.line:
            for x in self.cells:
                t.write(self.pixel, self._matrix[x][line])
        with t.line:
            for x in self.cells:
                t.write(self.pixel, self._matrix[x][line])


if __name__ == "__main__":
    m = Matrix(16, 12, auto_show=True, fill=BLACK)

    from bitmap import read_image

    m.set_pixels(read_image("./mario.bmp"))
