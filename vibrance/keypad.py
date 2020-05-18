import curses
import atexit

from . import interface


class KeypadInput:
    """Input device that reads keystrokes from the keyboard in a terminal
    window. Works on posix (Linux/MacOS) platforms only."""

    def __init__(self):
        """Creates a KeypadInput that receives keystrokes from the current
        window."""

        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)
        atexit.register(self.close)
        self.scr.addstr(1, 1, "Vibrance: Keypad Input")
        self.scr.refresh()

    def close(self):
        """Resets the terminal state."""
        self.scr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def __iter__(self):
        return self

    def __next__(self):
        return self.scr.getkey()


class KeypadInterface(interface.Interface):
    """Interface that launches user functions based on a KeypadInput."""

    def __init__(self):
        super().__init__()

        self.onKeyCallbacks = {}
        self.onNumberCallback = None
        self.onLetterCallback = None
        self.onSymbolCallback = None
        self.onSpecialCallback = None
        self.onAnyCallback = None

    def onKey(self, key):
        """Launches a user function when the given key is pressed."""
        def decorator(func):
            self.onKeyCallbacks[key] = func
            return func
        return decorator

    def onNumber(self, func):
        """Launches a user function when any number key is pressed."""
        self.onNumberCallback = func
        return func

    def onLetter(self, func):
        """Launches a user function when any letter key is pressed."""
        self.onLetterCallback = func
        return func

    def onSymbol(self, func):
        """Launches a user function when any symbol key is pressed."""
        self.onSymbolCallback = func
        return func

    def onSpecial(self, func):
        """Launches a user function when any special key (meta keys, arrow
        keys, etc) is pressed."""
        self.onSpecialCallback = func
        return func

    def onAny(self, func):
        """Launches a user function when any key is pressed."""
        self.onAnyCallback = func
        return func

    def run(self, keypad, ctrl):
        """Monitors for new keystrokes from the KeypadInput, launches user
        functions as necessary, and sends updates using the controller as
        necessary."""

        for key in keypad:
            if key in self.onKeyCallbacks:
                self.onKeyCallbacks[key](key)
                self.update(ctrl)
                continue

            if len(key) == 1:
                # Simple character
                if ord("0") <= ord(key) <= ord("9"):
                    if self.onNumberCallback:
                        self.onNumberCallback(key)
                        self.update(ctrl)
                        continue

                elif ord("a") <= ord(key) <= ord("z"):
                    if self.onLetterCallback:
                        self.onLetterCallback(key)
                        self.update(ctrl)
                        continue

                else:  # Symbol
                    if self.onSymbolCallback:
                        self.onSymbolCallback(key)
                        self.update(ctrl)
                        continue

            else:  # Complex key (arrows, numpad, etc)
                if self.onSpecialCallback:
                    self.onSpecialCallback(key)
                    self.update(ctrl)
                    continue

            if self.onAnyCallback:
                self.onAnyCallback(key)
                self.update(ctrl)
