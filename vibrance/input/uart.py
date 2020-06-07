import serial
import atexit


class SerialInput:
    """Input device that reads bytes from a serial port."""

    def __init__(self, name, port):
        """Creates a SerialInput that reads from the given port."""

        self.port = serial.Serial(port)
        atexit.register(self.port.close)

    def read(self):
        events = []
        while self.port.in_waiting > 0:
            byte = self.port.read().decode("utf-8")

            events.append({"input": "uart",
                           "type": "byte",
                           "byte": byte})

            events.append({"input": "uart",
                           "type": byte,
                           "byte": byte})

        return tuple(events)
