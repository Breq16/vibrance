import multiprocessing

from . import base

class PipeDriver(base.BaseDriver):
    """Input device that reads commands in a separate thread."""

    def __init__(self, name="", driver_type="pipe"):
        """Creates a PipeInput."""
        super().__init__(name)
        self.driver_type = driver_type

        self.in_pipe, self.out_pipe = multiprocessing.Pipe()

    def launch(self, event_type, obj={}):
        self.in_pipe.send((event_type, obj))

    def read(self):
        if not self.enabled:
            return tuple()
        events = []
        while self.out_pipe.poll():
            event_type, event_attrs = self.out_pipe.recv()

            events.append({"driver": self.driver_type,
                           "type": event_type, **event_attrs})

        return tuple(events)

    def getStatus(self):
        status = {}

        if self.enabled:
            status["health"] = "success"
            status["message"] = "Pipe Enabled"
        else:
            status["health"] = "inactive"
            status["message"] = "Pipe Disabled"

        return status
