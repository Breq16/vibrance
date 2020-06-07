import os
import atexit

import mido

from base_input import BaseInput

class MidiInput(BaseInput):
    """Input device that reads messages from a MIDI device."""

    def __init__(self, name="", portname="vibrance"):
        """Creates a MidiInput that receives messages from the given port.

        Linux/MacOS: Creates a virtual input port with the given name.

        Windows: Attempts to connect to a loopback port with the given name.
        """

        super().__init__(name)

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

    def read(self):
        events = []
        for msg in self.midi.iter_pending():
            if msg.type not in ("note_on", "note_off"):
                return tuple()

            event_attrs = {"note": msg.note,
                           "velocity": msg.velocity,
                           "channel": msg.channel,
                           "time": msg.time}

            events.append({"input": "midi",
                           "type": msg.type, **event_attrs})

            events.append({"input": "midi",
                           "type": f"{msg.type}_{msg.note}", **event_attrs})

            octave = msg.note // 12 - 2

            events.append({"input": "midi",
                           "type": f"{msg.type}_oct_{octave}", **event_attrs})

        return tuple(events)
