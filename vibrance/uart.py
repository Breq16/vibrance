import serial
import atexit

from . import interface


class SerialInput:
    """Input device that reads bytes from a serial port."""

    def __init__(self, port):
        """Creates a SerialInput that reads from the given port."""

        self.port = serial.Serial(port)
        atexit.register(self.port.close)

    def __iter__(self):
        return self

    def __next__(self):
        return self.port.read()


class SerialInterface(interface.Interface):
    """Interface that launches user functions based on a SerialInput."""

    def __init__(self):
        super().__init__()

        self.onByteCallbacks = {}
        self.onAnyCallback = None

    def onByte(self, byte):
        """Launches a user function when the given byte is received."""
        def decorator(func):
            self.onByteCallbacks[byte] = func
            return func
        return decorator

    def onAny(self, func):
        """Launches a user function when any byte is received."""
        self.onAnyCallback = func
        return func

    def run(self, ser, ctrl):
        """Monitors for new bytes from the SerialInput, launches user functions
        as necessary, and sends updates using the controller as necessary."""

        for byte in ser:
            if byte in self.onByteCallbacks:
                self.onByteCallbacks[byte](byte)
                self.update(ctrl)
                continue

            if self.onAnyCallback:
                self.onAnyCallback(byte)
                self.update(ctrl)
