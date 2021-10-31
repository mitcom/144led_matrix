import colorsys
from itertools import cycle
from math import ceil
from random import randint
import time

from matrix import MatrixSmallPixelsWithGaps, BLACK


def partition(chunks):
    if chunks == 0:
        return

    step = 1 / chunks
    value = step
    while value < 1.0:
        yield value
        value += step


def mul(factor, iterable):
    return [min(factor - 1, ceil(factor * i)) for i in iterable]


def normalize(sequence, min_r, max_r):
    max_x = max(sequence)
    min_x = min(sequence)
    diff = max_x - min_x

    values = [(x - min_x) / diff for x in sequence]

    diff_r = max_r - min_r
    return [(v * diff_r) + min_r for v in values]


def symmetric_range(steps):
    values = [i * i for i in range(steps)]
    return values + values[::-1]


def next_cyclic(index, values):
    next_index = (index + 1) % len(values)
    return next_index, values[next_index]


if __name__ == "__main__":
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
                randint(0, PIGMENTS - 1) if shape[y][x] else None,
                randint(0, 2 * BRIGHTNESS) if shape[y][x] else None,
            ]
            for x in range(X)
        ]
        for y in range(Y)
    ]

    colors = list(partition(PIGMENTS))
    lightnesses = normalize(symmetric_range(BRIGHTNESS), 0.35, 0.9)

    while True:
        for y in m.rows:
            for x in m.cells:
                if shape[y][x]:
                    h_index, l_index = data_matrix[y][x]
                    h_index, hue = next_cyclic(h_index, colors)
                    l_index, lightness = next_cyclic(l_index, lightnesses)

                    data_matrix[y][x] = h_index, l_index

                    rgb = mul(256, colorsys.hls_to_rgb(hue, lightness, 0.5))
                    m.set_pixel(x, y, rgb)
        m.show()
        time.sleep(0.1)
