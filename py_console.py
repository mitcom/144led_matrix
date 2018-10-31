import time

import ansi


# PIXEL = '████  '
PIXEL_DOWN = '███ '
PIXEL_UP= '▄▄▄ '
# PIXEL = '▄ '


with ansi.terminal():
    LINES = 12
    for t in range(100):
        t and ansi.move_cursor_up(2*LINES)
        for y in range(LINES):
            for x in range (12):
                ansi.write(PIXEL_UP, (int(y * 256/12), min(0+t*4, 255), int(x * 256/12)))
            ansi.write()
            for x in range (12):
                ansi.write(PIXEL_DOWN, (int(y * 256/12), min(0+t*4, 255), int(x * 256/12)))
            ansi.write()
        time.sleep(0.05)
