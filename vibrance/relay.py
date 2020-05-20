import socket
import subprocess
import atexit
import time
import json
import threading
import traceback
import ssl
import selectors
import argparse
from multiprocessing.dummy import Pool as ThreadPool

parser = argparse.ArgumentParser(description="Run a Vibrance relay server "
                                 "(command server and client WebSocket "
                                 "servers).")

parser.add_argument("--psk", help="Optional password for the command server.")

parser.add_argument("--cert", help="SSL certificate for securing the "
                    "WebSockets and the command server.")

parser.add_argument("--key", help="SSL private key for securing the WebSockets"
                    " and the command server.")

args = parser.parse_args()


class socket_type:
    """Namespace for socket type identifiers to be used with selectors."""
    SERVER = 0  # server socket
    WAITING = 1  # awaiting authentication
    CLIENT = 2  # connected client


class ClientServer:
    """Server allowing clients to connect and receive updates."""

    def __init__(self, cert=None, key=None):
        """Creates a ClientServer. If cert and key are specified, uses SSL."""

        self.selector = selectors.DefaultSelector()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 9001))
        sock.listen(128)
        self.selector.register(sock, selectors.EVENT_READ,
                               socket_type.SERVER)

        if cert is not None and key is not None:
            self.websockify_proc = subprocess.Popen(["websockify", "9000",
                                                     f"localhost:9001",
                                                     f"--cert={args.cert}",
                                                     f"--key={args.key}"],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL)
        else:
            self.websockify_proc = subprocess.Popen(["websockify", "9000",
                                                     f"localhost:9001"],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL)

        atexit.register(self.websockify_proc.terminate)

        self.clients = {}
        self.lastMessage = {}

        self.pool = ThreadPool(32)

        self.messages = {}

    def accept(self, server):
        """Accepts a new client on the given server socket."""
        new_client, addr = server.accept()
        self.selector.register(new_client, selectors.EVENT_READ,
                               socket_type.WAITING)
        self.lastMessage[new_client] = time.time()

    def addToZone(self, client):
        try:
            data = client.recv(1024)
        except OSError:
            self.remove(client)
            return
        if len(data) == 0:
            self.remove(client)
            return

        zone = data.decode("utf-8", "ignore")

        self.selector.modify(client, selectors.EVENT_READ, socket_type.CLIENT)
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
        except ValueError:
            pass
        try:
            del self.lastMessage[client]
        except KeyError:
            pass
        try:
            client.close()
        except OSError:
            pass

    def handleMessage(self, client):
        """Handles an incoming message from a client."""
        try:
            data = client.recv(1024)
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

                if type == socket_type.SERVER:
                    self.accept(sock)
                elif type == socket_type.WAITING:
                    self.addToZone(sock)
                elif type == socket_type.CLIENT:
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
            client.send(msg.encode("utf-8"))
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


class ControllerServer:
    """Server allowing controllers to connect and submit updates."""

    def __init__(self, clientServer, psk=None, cert=None, key=None):
        """Creats a ControllerServer with the specified ClientServer to
        broadcast updates to. If psk is provided, password-protects the server.
        If cert and key are provided, encrypts the server with SSL."""

        self.clientServer = clientServer
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
                               socket_type.SERVER)

    def accept(self):
        """Accepts a new controller client."""
        new_client, addr = self.sock.accept()
        if self.psk is not None:
            self.selector.register(new_client,
                                   selectors.EVENT_READ,
                                   socket_type.WAITING)
        else:
            self.selector.register(new_client,
                                   selectors.EVENT_READ,
                                   socket_type.CLIENT)

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
                                 socket_type.CLIENT)
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

        telemetry = self.clientServer.broadcast(messages)
        client.send(json.dumps(telemetry).encode("utf-8"))

    def run(self):
        """Monitors for new connections or updates from controller clients and
        handles them appropriately."""

        while True:
            events = self.selector.select()

            for key, mask in events:
                client = key.fileobj
                type = key.data

                if type == socket_type.SERVER:
                    self.accept()
                elif type == socket_type.WAITING:
                    self.authenticate(client)
                elif type == socket_type.CLIENT:
                    self.handleUpdate(client)


def wrapLoop(loopfunc):
    """Wraps a thread in a wrapper function to restart it if it exits."""
    def wrapped():
        while True:
            try:
                loopfunc()
            except BaseException:
                print(f"Exception in thread {loopfunc}, restarting in 10s...")
                traceback.print_exc()
            else:
                print(f"Thread {loopfunc} exited, restarting in 10s...")
            time.sleep(10)
    return wrapped


clientServer = ClientServer(args.cert, args.key)
controllerServer = ControllerServer(clientServer, args.psk,
                                    args.cert, args.key)

clientServerThread = threading.Thread(
    target=wrapLoop(clientServer.run))
controllerServerThread = threading.Thread(
    target=wrapLoop(controllerServer.run))
clientCheckAliveThread = threading.Thread(
    target=wrapLoop(clientServer.handleCheckAlive))

clientServerThread.start()
controllerServerThread.start()
clientCheckAliveThread.start()

while True:
    time.sleep(1)
