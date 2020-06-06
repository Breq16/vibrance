import multiprocessing

from . import Interface

class PipeInput:
    """Input device that reads commands in a separate thread."""

    def __init__(self, name="pipe"):
        """Creates a PipeInput."""
        self.name = name

        self.in_pipe, self.out_pipe = multiprocessing.Pipe()

    def launch(self, event_type, obj={}):
        self.in_pipe.send((event_type, obj))

    def read(self):
        events = []
        while self.out_pipe.poll():
            event_type, event_attrs = self.out_pipe.recv()

            events.append({"input": self.name,
                           "type": event_type, **event_attrs})

        return tuple(events)
