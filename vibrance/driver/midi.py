import os
import atexit

import mido

from . import base

class MidiDriver(base.BaseDriver):
    """Input device that reads messages from a MIDI device."""

    def __init__(self, name="", portname="vibrance"):
        """Creates a MidiInput that receives messages from the given port.

        Linux/MacOS: Creates a virtual input port with the given name.

        Windows: Attempts to connect to a loopback port with the given name.
        """
        super().__init__(name)
        self.portname = portname

    def open(self):
        if os.name == "posix":
            self.midi = mido.open_input(self.portname, virtual=True)
        elif os.name == "nt":
            try:
                self.midi = mido.open_input(f"{self.portname} 3")
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

        atexit.register(self.close)
        super().open()

    def close(self):
        super().close()
        self.midi.close()
        self.midi = None

    def read(self):
        if not self.enabled:
            return tuple()
        events = []
        for msg in self.midi.iter_pending():
            if msg.type not in ("note_on", "note_off"):
                return tuple()

            event_attrs = {"note": msg.note,
                           "velocity": msg.velocity,
                           "channel": msg.channel,
                           "time": msg.time}

            events.append({"driver": "midi",
                           "type": msg.type, **event_attrs})

            events.append({"driver": "midi",
                           "type": f"{msg.type}_{msg.note}", **event_attrs})

            octave = msg.note // 12 - 2

            events.append({"driver": "midi",
                           "type": f"{msg.type}_oct_{octave}", **event_attrs})

        return tuple(events)

    def getStatus(self):
        status = {}

        if self.enabled:
            status["health"] = "success"
            status["message"] = "MIDI Enabled"
        else:
            status["health"] = "inactive"
            status["message"] = "MIDI Disabled"

        return status
