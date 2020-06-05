import socket
import ssl
import select
import logging
import json

class TolerantSocket:
    def __init__(self, debug_level=logging.CRITICAL):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(debug_level)
        self.logger.info("Created tolerant socket")

    def connect(self, host, port, psk=None, ssl_context=None):
        self.logger.info("Set target at %s:%i", host, port)
        self.host = host
        self.port = port
        self.psk = psk
        self.context = ssl_context

        self.makeSocket()

    def makeSocket(self):
        self.logger.info("Creating new socket object...")
        unwrapped = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        unwrapped.settimeout(2)

        if self.context:
            self.socket = self.context.wrap_socket(unwrapped, server_hostname=self.host)
        else:
            self.socket = unwrapped

        try:
            self.socket.connect((self.host, self.port))
        except (ConnectionError, socket.timeout) as e:
            self.logger.error("Connection failed: %s", e)
            self.socket.close()
            self.socket = None

        if self.psk and self.socket:
            self.logger.info("Attempting auth...")
            self.send(self.psk.encode("utf-8"))
            if self.socket:
                ret = self.recv(1024)
                if self.socket:
                    if ret == b"OK":
                        return
                    else:
                        self.socket.close()
                        self.socket = None

    def send(self, data):
        if self.socket:
            try:
                self.socket.send(data)
            except (ConnectionError, socket.timeout) as e:
                self.logger.error("Send failed: %s", e)
                self.socket.close()
                self.socket = None
            else:
                self.logger.debug("Send successful")
        else:
            self.logger.error("Failed to send, not connected")

    def recv(self, length):
        if self.socket:
            try:
                data = self.socket.recv(length)
            except (ConnectionError, socket.timeout) as e:
                self.logger.error("Recv failed: %s", e)
                self.socket.close()
                self.socket = None
            else:
                if len(data) == 0:
                    self.logger.error("Socket disconnected")
                    self.socket.close()
                    self.socket = None
                else:
                    self.logger.debug("Recv successful, returned %s", data)
                    return data
        else:
            self.logger.error("Failed to recv, not connected")

    def repair(self):
        if not self.socket:
            self.logger.info("Attempting repair...")
            self.makeSocket()

    def recvJSON(self, length=1024):
        data = self.recv(length)
        if data:
            try:
                data = data.decode("utf-8")
            except UnicodeDecodeError:
                self.logger.error("Invalid UTF-8 received")
            else:
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    self.logger.error("Invalid JSON received")
                else:
                    return data
