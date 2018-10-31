import contextlib
import sys
import termios

LF = '\n'
_ESC = '\x1b'
_CSI = f'{_ESC}['

_TERMIOS_LFLAGS_ID = 3  # termios local-mode flags index


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

def write(text, color=None, reset=False, new_line=False):
    ansi_text = _ansi_text(text, color, reset)
    line_feed = LF if new_line else ''
    sys.stdout.write(f'{ansi_text}{line_feed}')

def line_feed():
    sys.stdout.write(LF)

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


class Echo:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.original_tty_attributes = termios.tcgetattr(self.fd)

    def switch_off(self):
        tty_attributes = self.original_tty_attributes[:]
        tty_attributes[_TERMIOS_LFLAGS_ID] = (
            tty_attributes[_TERMIOS_LFLAGS_ID] & ~termios.ECHO
        )
        termios.tcsetattr(self.fd, termios.TCSADRAIN, tty_attributes)

    def reset(self):
        termios.tcsetattr(
            self.fd, termios.TCSADRAIN, self.original_tty_attributes,
        )


class Terminal:
    def __init__(self):
        self.written_lines = 0

    def write(self, text, *args, new_line=False, **kwargs):
        self.written_lines += text.count(LF) + new_line
        return write(text, *args, new_line, **kwargs)

    def break_line(self):
        self.written_lines += 1
        return line_feed()

    def go_to_origin(self):
        if self.written_lines:
            move_cursor_up(self.written_lines)
            self.written_lines = 0


@contextlib.contextmanager
def terminal():
    echo = Echo()
    terminal = Terminal()

    try:
        hide_cursor()
        echo.switch_off()

        yield terminal

    finally:
        show_cursor()
        reset()
        echo.reset()
