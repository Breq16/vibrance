import os
import atexit

import mido

class MidiInput:
    def __init__(self):
        if os.name == "posix":
            self.midi = mido.open_input("vibrance", virtual=True)
        elif os.name == "nt":
            self.midi = mido.open_input("vibrance 3")
        else:
            raise ValueError("unsupported OS")

        atexit.register(self.midi.close)

    def __iter__(self):
        return iter(self.midi)
