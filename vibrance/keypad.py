import curses
import atexit

from . import interface


class KeypadInput:
    def __init__(self):
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.scr.keypad(True)
        atexit.register(self.close)
        self.scr.addstr(1, 1, "Vibrance: Keypad Input")
        self.scr.refresh()

    def close(self):
        self.scr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def __iter__(self):
        return self

    def __next__(self):
        return self.scr.getkey()


class KeypadInterface(interface.Interface):
    def __init__(self):
        super().__init__()

        self.onKeyCallbacks = {}
        self.onNumberCallback = None
        self.onLetterCallback = None
        self.onSymbolCallback = None
        self.onSpecialCallback = None
        self.onAnyCallback = None

    def onKey(self, key):
        def decorator(func):
            self.onKeyCallbacks[key] = func
            return func
        return decorator

    def onNumber(self, func):
        self.onNumberCallback = func
        return func

    def onLetter(self, func):
        self.onLetterCallback = func
        return func

    def onSymbol(self, func):
        self.onSymbolCallback = func
        return func

    def onSpecial(self, func):
        self.onSpecialCallback = func
        return func

    def onAny(self, func):
        self.onAnyCallback = func
        return func

    def run(self, keypad, ctrl):
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
