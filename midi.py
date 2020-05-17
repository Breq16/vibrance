import interface

class MidiInterface(interface.Interface):
    def __init__(self):
        super().__init__()

        self.onNoteCallbacks = {}
        self.onOctaveCallbacks = {}
        self.onAnyCallback = None
        self.onTelemetryCallback = None

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
