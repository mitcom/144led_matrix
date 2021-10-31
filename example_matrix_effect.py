from random import randint
import time

from matrix import Matrix, BLACK

WORLD_SIZE = 50
GREEN = [128, 255, 128]


def dim(value):
    return int(value / 1.5)


def next_cycle(matrix):
    for column in range(WORLD_SIZE):
        if not randint(0, 20):
            matrix[WORLD_SIZE - 1][column] = GREEN

    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if not cell == BLACK:
                r, g, b = cell
                matrix[y][x] = (dim(r), dim(g), dim(b))
                matrix[y - 1][x] = cell


if __name__ == "__main__":
    data_matrix = [
        [BLACK if randint(0, 8) else GREEN for x in range(WORLD_SIZE)]
        for y in range(WORLD_SIZE)
    ]

    m = Matrix(WORLD_SIZE, WORLD_SIZE, auto_show=False, fill=BLACK)

    while True:
        for y in m.rows:
            for x in m.cells:
                m.set_pixel(x, y, data_matrix[abs(y - WORLD_SIZE) - 1][x])
            m.show()
        next_cycle(data_matrix)
        time.sleep(0.02)
