import serial
import serial.tools.list_ports
import atexit

from . import base

def list_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

class SerialDriver(base.BaseDriver):
    """Input device that reads bytes from a serial port."""

    def __init__(self, name="", portname=""):
        """Creates a SerialInput that reads from the given port."""
        super().__init__(name)
        self.portname = portname

    def open(self):
        self.port = serial.Serial(self.portname)
        atexit.register(self.close)
        super().open()

    def close(self):
        super().close()
        self.port.close()

    def read(self):
        if not self.enabled:
            return tuple()
        events = []
        while self.port.in_waiting > 0:
            byte = self.port.read().decode("utf-8")

            events.append({"driver": "uart",
                           "type": "byte",
                           "byte": byte})

            events.append({"driver": "uart",
                           "type": byte,
                           "byte": byte})

        return tuple(events)

    def getStatus(self):
        status = {}

        if self.enabled:
            status["health"] = "success"
            status["message"] = "Serial Enabled"
        else:
            status["health"] = "inactive"
            status["message"] = "Serial Disabled"

        return status
