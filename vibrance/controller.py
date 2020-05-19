import socket
import json
import time
import ssl


class Controller:
    """Manages a connection with a relay server and sends new messages."""

    def __init__(self):
        pass

    def connect(self, relay, psk=None, enable_ssl=True):
        """Connects to a relay server at the given address. If psk is provided,
        log into the relay using the password. If enable_ssl is provided,
        connect to the server using SSL."""

        if enable_ssl:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.context.load_default_certs()
            unwrapped_socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
            self.socket = self.context.wrap_socket(unwrapped_socket,
                                                   server_hostname=relay)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((relay, 9999))

        if psk:
            self.socket.send(psk.encode("utf-8"))
            ret = self.socket.recv(1024)
            if ret == b"OK":
                return
            else:
                raise ValueError("authentication failed")

    def write(self, messages):
        """Send messages to the relay server to be broadcasted to clients.
        Returns performance data from both the relay server and local
        measurements."""

        timestamp = time.time()
        self.socket.send((json.dumps(messages)+"\n").encode("utf-8"))
        stats = {}
        stats["server"] = json.loads(self.socket.recv(1024).decode("utf-8"))
        stats["controller"] = {"latency": int((time.time()-timestamp)*1000)}
        return stats
