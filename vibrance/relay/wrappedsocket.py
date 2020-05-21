import socket
import ssl
import json

from websockify import websocket

class ClientDisconnected(OSError):
    pass

class BinaryWebSocket(websocket.WebSocket):
    def select_subprotocol(self, protocols):
        return "binary"

class WrappedSocket:
    def __init__(self, sock, ssl_context=None):
        print("Doing handshake...")
        self.sock = sock

        # Determine if connection uses SSL
        handshake = self.sock.recv(1024, socket.MSG_PEEK)

        if not handshake:
            sock.close()
            raise ClientDisconnected("No handshake received")

        if handshake[0] in (0x16, 0x80):
            # Connection uses SSL
            if not ssl_context:
                sock.close()
                raise ClientDisconnected("Client attempted to connect via SSL but server does not support")
            self.unwrapped = sock
            self.sock = ssl_context.wrap_socket(sock, server_side=True)

        request = self.sock.recv(1024).decode("utf-8", "ignore")

        print(request)

        headers = {(k.lower() if k == "Upgrade" else k): v.strip() for k, v in [line.split(":", 1) for line in request.splitlines() if ":" in line]}

        print(headers)

        self.websock = BinaryWebSocket()

        self.websock.accept(self.sock, headers)


    def recv(self):
        try:
            return self.websock.recvmsg()
        except websocket.WebSocketWantReadError:
            print("Socket reports read necessary but no data!")
            return None

    def send(self, msg):
        self.websock.sendmsg(msg)

    def close(self):
        # TODO: shutdown gracefully
        #self.websock.shutdown(None)
        # workaround: shutdown violently
        self.websock.close()
