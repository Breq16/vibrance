import os
import atexit

import mido

from . import interface


class MidiInput:
    def __init__(self, name):
        if os.name == "posix":
            self.midi = mido.open_input(name, virtual=True)
        elif os.name == "nt":
            try:
                self.midi = mido.open_input(f"{name} 3")
            except OSError as e:
                raise OSError("It looks like you're trying to use Vibrance's "
                              "MIDI interface on a Windows device. Vibrance "
                              "MIDI uses 'virtual' MIDI ports in order to "
                              "function properly. However, Windows does not "
                              "support virtual ports. Please install the "
                              "program 'loopMIDI' and create a loopback "
                              "port manually before running Vibrance.") from e
        else:
            raise ValueError("unsupported OS")

        atexit.register(self.midi.close)

    def __iter__(self):
        return iter(self.midi)


class MidiInterface(interface.Interface):
    def __init__(self):
        super().__init__()

        self.onNoteCallbacks = {}
        self.onOctaveCallbacks = {}
        self.onAnyCallback = None

    def onNote(self, note):
        def decorator(func):
            self.onNoteCallbacks[note] = func
            return func
        return decorator

    def onOctave(self, octave):
        octave += 2

        def decorator(func):
            self.onOctaveCallbacks[octave] = func
            return func
        return decorator

    def onAny(self, func):
        self.onAnyCallback = func
        return func

    def run(self, midi, ctrl):
        for msg in midi:
            if msg.type == "note_on":
                if msg.note in self.onNoteCallbacks:
                    self.onNoteCallbacks[msg.note](msg)
                    self.update(ctrl)
                    continue

                octave = msg.note // 12
                if octave in self.onOctaveCallbacks:
                    self.onOctaveCallbacks[octave](msg)
                    self.update(ctrl)
                    continue

                if self.onAnyCallback:
                    self.onAnyCallback(msg)
                    self.update(ctrl)
