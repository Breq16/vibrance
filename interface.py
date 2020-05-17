class Interface:
    def __init__(self):
        self.clear()

    def clear(self):
        self.messages = {}
        self.delay = 0

    def add(self, port, color=None, **kwargs):
        if port not in self.messages:
            self.messages[port] = []

        message = {}
        if color is not None:
            message["color"] = color

        for key, val in kwargs.items():
            message[key] = val

        self.messages[port].append(message)

    def color(self, ports, color):
        if hasattr(ports, "__iter__"):
            for port in ports:
                self.add(port, color, delay=self.delay)
        else:
            self.add(ports, color, delay=self.delay)

    def wait(self, sec):
        self.delay += sec * 1000

    def update(self, ctrl):
        ctrl.messages = self.messages
        ctrl.write()
        self.clear()
