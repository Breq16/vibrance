import os
import atexit

import mido

from .. import controller

class NoUpdate:
    pass

class Interface(controller.Controller):
    def __init__(self, host):
        super().__init__(host)

        if os.name == "posix":
            self.midi = mido.open_input("vibrance", virtual=True)
        elif os.name == "nt":
            self.midi = mido.open_input("vibrance 3")
        else:
            raise ValueError("unsupported OS")

        atexit.register(self.midi.close)

        self.triggers = {}
        self.onAnyCallback = None
        self.onTelemetryCallback = None

    def _wrapUpdate(self, func, msg=None):
        self.clear()
        if msg is not None:
            result = func(msg)
        else:
            result = func(msg)
        if not isinstance(result, NoUpdate):
            telemetry = self.write()
            if self.onTelemetryCallback:
                self.onTelemetryCallback(telemetry)

    def onTrigger(self, note):
        def decorator(func):
            def wrapper():
                self._wrapUpdate(func)
            self.triggers[note] = wrapper
            return wrapper
        return decorator

    def onAny(self, func):
        def wrapper(msg):
            self._wrapUpdate(func, msg)
        self.onAnyCallback = wrapper
        return wrapper

    def onTelemetry(self, func):
        self.onTelemetryCallback = func
        return func

    def run(self):
        for msg in self.midi:
            if msg.type == "note_on":
                if self.onAnyCallback:
                    self.onAnyCallback(msg)
                else:
                    if msg.note in self.triggers:
                        self.triggers[msg.note]()
