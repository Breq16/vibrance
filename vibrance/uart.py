import serial
import atexit

from . import interface


class SerialInput:
    def __init__(self, port):
        self.port = serial.Serial(port)
        atexit.register(self.port.close)

    def __iter__(self):
        return self

    def __next__(self):
        return self.port.read()


class SerialInterface(interface.Interface):
    def __init__(self):
        super().__init__()

        self.onByteCallbacks = {}
        self.onAnyCallback = None

    def onByte(self, byte):
        def decorator(func):
            self.onByteCallbacks[byte] = func
            return func
        return decorator

    def onAny(self, func):
        self.onAnyCallback = func
        return func

    def run(self, ser, ctrl):
        for byte in ser:
            if byte in self.onByteCallbacks:
                self.onByteCallbacks[byte](byte)
                self.update(ctrl)
                continue

            if self.onAnyCallback:
                self.onAnyCallback(byte)
                self.update(ctrl)
