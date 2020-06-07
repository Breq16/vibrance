import multiprocessing

from . import base_input

class PipeInput(base_input.BaseInput):
    """Input device that reads commands in a separate thread."""

    def __init__(self, name="", input_type="pipe"):
        """Creates a PipeInput."""
        super().__init__(name)
        self.input_type = input_type

        self.in_pipe, self.out_pipe = multiprocessing.Pipe()

        self.enabled = False

    def open(self):
        self.enabled = True

    def close(self):
        self.enabled = False

    def launch(self, event_type, obj={}):
        self.in_pipe.send((event_type, obj))

    def read(self):
        if not self.enabled:
            return tuple()
        events = []
        while self.out_pipe.poll():
            event_type, event_attrs = self.out_pipe.recv()

            events.append({"input": self.input_type,
                           "type": event_type, **event_attrs})

        return tuple(events)
