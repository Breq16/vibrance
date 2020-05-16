import os
import atexit

import mido

import controller

class NoUpdate:
    pass

class Interface(controller.Controller):
    def __init__(self):
        super().__init__()

        if os.name == "posix":
            self.midi = mido.open_input("vibrance", virtual=True)
        elif os.name == "nt":
            self.midi = mido.open_input("vibrance 3")
        else:
            raise ValueError("unsupported OS")

        atexit.register(self.midi.close)

        self.onNoteCallbacks = {}
        self.onOctaveCallbacks = {}
        self.onAnyCallback = None
        self.onTelemetryCallback = None

    def update(self):
        telemetry = self.write()
        self.clear()
        if self.onTelemetryCallback:
            self.onTelemetryCallback(telemetry)
        return telemetry

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

    def onTelemetry(self, func):
        self.onTelemetryCallback = func
        return func

    def run(self):
        for msg in self.midi:
            if msg.type == "note_on":
                if msg.note in self.onNoteCallbacks:
                    self.onNoteCallbacks[msg.note](msg)
                    continue

                octave = msg.note // 12
                if octave in self.onOctaveCallbacks:
                    self.onOctaveCallbacks[octave](msg)
                    continue

                if self.onAnyCallback:
                    self.onAnyCallback(msg)
