import curses
import atexit
import string

from . import base

class KeypadDriver(base.BaseDriver):
    """Input device that reads keystrokes from the keyboard in a terminal
    window. Works on posix (Linux/MacOS) platforms only."""

    def __init__(self, name=""):
        super().__init__(name)
        self.ready = False

    def open(self):
        """Creates a KeypadInput that receives keystrokes from the current
        window."""
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)
        self.scr.nodelay(True)
        atexit.register(self.close)
        self.scr.addstr(1, 1, "Vibrance: Keypad Input")
        self.scr.refresh()
        self.ready = True

    def close(self):
        """Resets the terminal state."""
        self.ready = False
        self.scr.nodelay(False)
        self.scr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def read(self):
        if not self.ready:
            return tuple()
        events = []
        while True:
            try:
                key = self.scr.getkey()
            except curses.error: # No input to process
                break

            if key in string.ascii_letters:
                key_type = "letter"
            elif key in string.digits:
                key_type = "number"
            elif key in string.punctuation:
                key_type = "symbol"
            else:
                key_type = "special"

            events.append({"driver": "keypad",
                           "type": "keydown",
                           "key": key})

            events.append({"driver": "keypad",
                           "type": key_type,
                           "key": key})

            events.append({"driver": "keypad",
                           "type": f"key_{key}",
                           "key": key})

        return tuple(events)
