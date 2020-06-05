import socket
import selectors
import json
import time
import ssl

from . import tolerant_socket

class Controller:
    """Manages a connection with a relay server and sends new messages."""

    def __init__(self):
        self.connected = False

    def connect(self, relay, psk=None, enable_ssl=True):
        """Connects to a relay server at the given address. If psk is provided,
        log into the relay using the password. If enable_ssl is provided,
        connect to the server using SSL."""

        if enable_ssl:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_default_certs()
        else:
            context = None

        self.socket = tolerant_socket.TolerantSocket()
        self.socket.connect(relay, 9999, psk, context)

    def write(self, messages):
        """Send messages to the relay server to be broadcasted to clients.
        Returns performance data from both the relay server and local
        measurements."""

        self.socket.repair()

        timestamp = time.time()
        self.socket.send((json.dumps(messages)+"\n").encode("utf-8"))

        stats = {}
        stats["server"] = self.socket.recvJSON()
        stats["controller"] = {"latency": int((time.time()-timestamp)*1000)}
        return stats
