from . import interface


class SerialInput:
    def __init__(self, port):
        self.port = port


class SerialInterface(interface.Interface):
    def __init__(self):
        super().__init__()
