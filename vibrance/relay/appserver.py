import socket
import ssl
import json
from multiprocessing.dummy import Pool as ThreadPool

from . import wrappedsocket


class AppServer:
    """Server allowing clients to connect and receive updates."""

    # Constants used to indicate socket type when used with selectors:
    SERVER = 0  # server socket
    WAITING = 1  # awaiting authentication
    CLIENT = 2  # connected client

    def __init__(self, cert=None, key=None):
        """Creates an AppServer. If cert and key are specified, uses SSL."""

        if cert is not None and key is not None:
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(cert, key)
        else:
            self.ssl_context = None

        self.selector = selectors.DefaultSelector()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", 9000))
        sock.listen(16)
        self.selector.register(sock, selectors.EVENT_READ,
                               AppServer.SERVER)

        self.wrappedSockets = {}

        self.clients = {}
        self.lastMessage = {}

        self.pool = ThreadPool(32)

        self.messages = {}

    def accept(self, server):
        """Accepts a new client on the given server socket."""
        new_client, addr = server.accept()
        wrapped = wrappedsocket.WrappedSocket(new_client, self.ssl_context)

        self.selector.register(new_client, selectors.EVENT_READ,
                               AppServer.WAITING)
        self.wrappedSockets[new_client] = wrapped
        self.lastMessage[new_client] = time.time()

    def addToZone(self, client):
        try:
            data = self.wrappedSockets[client].recv()
        except OSError:
            self.remove(client)
            return
        if len(data) == 0:
            self.remove(client)
            return

        zone = data.decode("utf-8", "ignore")

        self.selector.modify(client, selectors.EVENT_READ, AppServer.CLIENT)
        self.clients[client] = zone
        self.lastMessage[client] = time.time()

    def remove(self, client):
        """Removes a client from all lists and closes it if possible."""
        try:
            self.selector.unregister(client)
        except KeyError:
            pass
        try:
            del self.clients[client]
        except KeyError:
            pass
        try:
            del self.lastMessage[client]
        except KeyError:
            pass
        try:
            self.wrappedSockets[client].close()
        except OSError:
            pass

    def handleMessage(self, client):
        """Handles an incoming message from a client."""
        try:
            data = self.wrappedSockets[client].recv()
        except OSError:
            self.remove(client)
            return
        if len(data) == 0:  # Client disconnected
            self.remove(client)
            return

        msg = data.decode("utf-8", "ignore")

        if msg == "OK":
            self.lastMessage[client] = time.time()
        else:
            self.remove(client)
            return

    def run(self):
        """Monitors for new client connections or messages and handles them
        appropriately."""
        while True:
            events = self.selector.select()
            for key, mask in events:
                sock = key.fileobj
                type = key.data

                if type == AppServer.SERVER:
                    self.accept(sock)
                elif type == AppServer.WAITING:
                    self.addToZone(sock)
                elif type == AppServer.CLIENT:
                    self.handleMessage(sock)

    def handleCheckAlive(self):
        """Periodically checks each client to ensure they are still alive
        and sending messages."""
        while True:
            clients = list(self.clients.keys())
            for client in clients:
                try:
                    if time.time() - self.lastMessage[client] > 20:
                        self.remove(client)
                except KeyError:  # Client was already removed
                    pass
                time.sleep(10 / len(clients))

    def broadcastToClient(self, item):
        """Broadcasts the appropriate current message to a single client."""
        client, zone = item
        if zone not in self.messages:
            return
        msg = json.dumps(self.messages[zone])
        try:
            self.wrappedClients[client].send(msg.encode("utf-8"))
        except OSError:
            self.remove(client)

    def broadcast(self, messages):
        """Broadcasts the given messages to all clients."""
        ts = time.time()
        self.messages = messages
        self.pool.map(self.broadcastToClient, self.clients.items())
        telemetry = {"clients": len(self.clients),
                     "latency": int((time.time() - ts)*1000)}
        return telemetry
