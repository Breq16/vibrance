import multiprocessing

from . import Interface

class PipeInput:
    """Input device that reads commands in a separate thread."""

    def __init__(self):
        """Creates a PipeInput."""

        self.in_pipe, self.out_pipe = multiprocessing.Pipe()

    def launch(self, funcname, obj=None):
        self.in_pipe.send((funcname, obj))

    def __iter__(self):
        return self

    def __next__(self):
        return self.out_pipe.recv()


class PipeInterface(Interface):
    """Interface that launches user functions based on a PipeInput."""

    def __init__(self):
        super().__init__()

        self.callbacks = {}

    def handle(self, func):
        """Launches a user function when it is called by code on the other
        end of the Pipe."""
        self.callbacks[func.__name__] = func
        return func

    def run(self, pipe, ctrl):
        """Monitors for new commands from the PipeInput, launches user
        functions as necessary, and sends updates using the controller as
        necessary."""

        for funcname, obj in pipe:
            if funcname in self.callbacks:
                if self.callbacks[funcname].__code__.co_argcount > 0:
                    self.callbacks[funcname](obj)
                else:
                    self.callbacks[funcname]()
                self.update(ctrl)
