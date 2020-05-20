import socket
import json
import ssl
import selectors


class ControlServer:
    """Server allowing controllers to connect and submit updates."""

    # Constants used to indicate socket type when used with selectors:
    SERVER = 0  # server socket
    WAITING = 1  # awaiting authentication
    CLIENT = 2  # connected client

    def __init__(self, appServer, psk=None, cert=None, key=None):
        """Creats a ControlServer with the specified ClientServer to
        broadcast updates to. If psk is provided, password-protects the server.
        If cert and key are provided, encrypts the server with SSL."""

        self.appServer = appServer
        self.psk = psk

        if cert is not None and key is not None:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_default_certs()
            self.ssl_context.load_cert_chain(cert, key)

            self.sock_unwrapped = socket.socket(socket.AF_INET,
                                                socket.SOCK_STREAM)
            self.sock_unwrapped.setsockopt(socket.SOL_SOCKET,
                                           socket.SO_REUSEADDR, 1)
            self.sock_unwrapped.bind(("0.0.0.0", 9999))
            self.sock_unwrapped.listen(16)

            self.sock = self.ssl_context.wrap_socket(self.sock_unwrapped,
                                                     server_side=True)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", 9999))
            self.sock.listen(16)

        self.selector = selectors.DefaultSelector()
        self.selector.register(self.sock, selectors.EVENT_READ,
                               ControlServer.SERVER)

    def accept(self):
        """Accepts a new controller client."""
        new_client, addr = self.sock.accept()
        if self.psk is not None:
            self.selector.register(new_client,
                                   selectors.EVENT_READ,
                                   ControlServer.WAITING)
        else:
            self.selector.register(new_client,
                                   selectors.EVENT_READ,
                                   ControlServer.CLIENT)

    def remove(self, client):
        """Removes a controller client from all lists and closes it if
        possible."""

        self.selector.unregister(client)
        try:
            client.close()
        except OSError:
            pass

    def authenticate(self, client):
        """Handles messages from a controller client that needs to
        authenticate."""

        try:
            data = client.recv(1024)
        except OSError:
            self.remove(client)
            return
        if len(data) == 0:
            self.remove(client)
            return

        msg = data.decode("utf-8", "ignore")
        if msg == self.psk:
            self.selector.modify(client, selectors.EVENT_READ,
                                 ControlServer.CLIENT)
            client.send(b"OK")
        else:
            self.remove(client)

    def handleUpdate(self, client):
        """Handles update messages from a connected controller client."""
        try:
            data = client.recv(2**18)
        except OSError:
            self.remove(client)
            return
        if len(data) == 0:
            self.remove(client)
            return

        msg = data.decode("utf-8", "ignore")

        try:
            messages = json.loads(msg.split("\n")[0])
        except json.JSONDecodeError:
            self.remove(client)
            return

        telemetry = self.appServer.broadcast(messages)
        client.send(json.dumps(telemetry).encode("utf-8"))

    def run(self):
        """Monitors for new connections or updates from controller clients and
        handles them appropriately."""

        while True:
            events = self.selector.select()

            for key, mask in events:
                client = key.fileobj
                type = key.data

                if type == ControlServer.SERVER:
                    self.accept()
                elif type == ControlServer.WAITING:
                    self.authenticate(client)
                elif type == ControlServer.CLIENT:
                    self.handleUpdate(client)
