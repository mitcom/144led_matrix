from random import randint
import time

from matrix import Matrix, BLACK

WORLD_SIZE = 50
CYCLE_TIME = 0.1
INITIAL_LIFE_RATIO = 5


SPACE = BLACK
LIFE = (255, 255, 255)


def get_neighbors(world, x, y):
    edge = WORLD_SIZE - 1
    try:
        neighbors = [
            world[y - 1][x - 1] if 0 <= x and 0 <= y else 0,
            world[y - 1][x] if 0 <= y else 0,
            world[y - 1][x + 1] if x < edge and 0 <= y else 0,
            world[y][x - 1] if 0 <= x else 0,
            world[y][x + 1] if x < edge else 0,
            world[y + 1][x - 1] if 0 <= x and y < edge else 0,
            world[y + 1][x] if 0 <= y < edge else 0,
            world[y + 1][x + 1] if x < edge and y < edge else 0,
        ]
    except IndexError:
        print(x, y)

    return sum(neighbors)


def has_survived(is_living, living_neighbor):
    if is_living:
        return True if 2 <= living_neighbor <= 3 else False

    return True if living_neighbor == 3 else False


def next_cycle(world):
    new_state = [
        [has_survived(cell, get_neighbors(world, x, y)) for x, cell in enumerate(row)]
        for y, row in enumerate(world)
    ]
    return new_state


if __name__ == "__main__":

    data_matrix = [
        [
            True if not randint(0, INITIAL_LIFE_RATIO) else False
            for x in range(WORLD_SIZE)
        ]
        for y in range(WORLD_SIZE)
    ]

    m = Matrix(WORLD_SIZE, WORLD_SIZE, auto_show=False, fill=BLACK)

    while True:
        for y in m.rows:
            for x in m.cells:
                m.set_pixel(x, y, LIFE if data_matrix[y][x] else SPACE)
            m.show()
        data_matrix = next_cycle(data_matrix)
        time.sleep(0.1)
