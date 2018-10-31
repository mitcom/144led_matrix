import time

import ansi


# PIXEL = '████  '
PIXEL_DOWN = '███ '
PIXEL_UP= '▄▄▄ '
# PIXEL = '▄ '


with ansi.terminal() as terminal:
    LINES = 12
    for t in range(100):
        terminal.go_to_origin()
        for y in range(LINES):
            for x in range (12):
                terminal.write(
                    PIXEL_UP,
                    (int(y * 256/12), min(0+t*4, 255), int(x * 256/12)),
                )
            terminal.break_line()
            for x in range(12):
                terminal.write(
                    PIXEL_DOWN,
                    (int(y * 256/12), min(0+t*4, 255), int(x * 256/12)),
                )
            terminal.break_line()
        time.sleep(0.05)
