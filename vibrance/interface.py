class Interface:
    """Provides a user-friendly API for creating color messages and launching
    user functions based on input."""

    def __init__(self):
        self.clear()
        self.onTelemetryCallback = None

    def clear(self):
        """Clears the messages buffer and resets the delay offset."""
        self.messages = {}
        self.delay = 0

    def add(self, port, color=None, **kwargs):
        """Adds a new message to the messages buffer."""

        if port not in self.messages:
            self.messages[port] = []

        message = {}
        if color is not None:
            message["color"] = color

        for key, val in kwargs.items():
            message[key] = val

        self.messages[port].append(message)

    def color(self, ports, color):
        """Creates a message to show the given color on the given ports after
        the delay offset."""

        if hasattr(ports, "__iter__"):
            for port in ports:
                self.add(port, color, delay=self.delay)
        else:
            self.add(ports, color, delay=self.delay)

    def wait(self, sec):
        """Adds to the current delay offset."""
        self.delay += sec * 1000

    def onTelemetry(self, func):
        """Launches the function when new telemetry data is received."""
        self.onTelemetryCallback = func
        return func

    def update(self, ctrl):
        """Sends the current messages to a relay through the provided
        controller, then clears the internal message buffer and delay
        offset."""
        telemetry = ctrl.write(self.messages)
        if self.onTelemetryCallback:
            self.onTelemetryCallback(telemetry)
        self.clear()
