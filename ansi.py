import contextlib
import sys

_ESC = '\x1b'
_CSI = f'{_ESC}['

def _sgr(parameter):
    return f'{_CSI}{parameter}m'

def _reset_code():
    return _sgr(0)

def _rgb(r, g, b):
    return f'2;{r};{g};{b}'

def _foreground(r, g, b):
    rgb_sequence = _rgb(r, g, b)
    return _sgr(f'38;{rgb_sequence}')

def _ansi_text(text, color=None, reset=False):
    foreground_color = _foreground(*color) if color else ''
    reset_sequence = _reset_code() if reset else ''

    return f'{foreground_color}{text}{reset_sequence}'

def write(text='', color=None, reset=False, new_line=False):
    if text:
        ansi_text = _ansi_text(text, color, reset)
        line_feed = '\n' if new_line else ''
        sentence = f'{ansi_text}{line_feed}'
    else:
        sentence = '\n'
    sys.stdout.write(f'{sentence}')

def move_cursor_up(cells_number):
    sentence = f'{_CSI}{cells_number}A'
    sys.stdout.write(sentence)

def hide_cursor():
    sentence = f'{_CSI}?25l'
    sys.stdout.write(sentence)

def show_cursor():
    sentence = f'{_CSI}?25h'
    sys.stdout.write(sentence)

def reset():
    sys.stdout.write(_reset_code())

@contextlib.contextmanager
def terminal():
    try:
        hide_cursor()
        yield
    finally:
        write()
        show_cursor()
        reset()
