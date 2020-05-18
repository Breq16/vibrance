import os
import atexit

import mido

from . import interface


class MidiInput:
    """Input device that reads messages from a MIDI device."""

    def __init__(self, name):
        """Creates a MidiInput that receives messages from the given port.

        Linux/MacOS: Creates a virtual input port with the given name.

        Windows: Attempts to connect to a loopback port with the given name.
        """

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
    """Interface that launches user functions based on a MidiInput."""

    def __init__(self):
        super().__init__()

        self.onNoteCallbacks = {}
        self.onOctaveCallbacks = {}
        self.onAnyCallback = None

    def onNote(self, note):
        """Launches a user function when the given note is received."""
        def decorator(func):
            self.onNoteCallbacks[note] = func
            return func
        return decorator

    def onOctave(self, octave):
        """Launches a user function when a note in the given octave is
        received."""
        octave += 2

        def decorator(func):
            self.onOctaveCallbacks[octave] = func
            return func
        return decorator

    def onAny(self, func):
        """Launches a user function when any note is received."""
        self.onAnyCallback = func
        return func

    def run(self, midi, ctrl):
        """Monitors for new notes from the MidiInput, launches user functions
        as necessary, and sends updates using the controller as necessary."""

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
