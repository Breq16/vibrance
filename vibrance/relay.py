import socket
import subprocess
import atexit
import time
import json
import threading
import traceback
import ssl
import os
import pathlib
import selectors
import argparse
from multiprocessing.dummy import Pool as ThreadPool

parser = argparse.ArgumentParser()
parser.add_argument("--psk", help="Optional password to protect the command server.")
parser.add_argument("--cert", help="SSL certificate for secure WebSockets.")
parser.add_argument("--key", help="SSL private key for secure WebSockets.")
args = parser.parse_args()

if args.cert is not None and args.key is not None:
    enable_ssl = True

ports = list(range(9001, 9007))
messages = {}
servers = []
clients = []
lastMessage = {}
websockify_procs = []

serverSelector = selectors.DefaultSelector()
clientSelector = selectors.DefaultSelector()

for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", port+100))
    sock.listen(16)
    servers.append(sock)
    serverSelector.register(sock, selectors.EVENT_READ)

for port in ports:
    # Start the websockify
    if enable_ssl:
        websockify_procs.append(subprocess.Popen(["websockify", str(port),
                                                  f"localhost:{port+100}",
                                                  f"--cert={args.cert}",
                                                  f"--key={args.key}"],
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.DEVNULL))
    else:
        websockify_procs.append(subprocess.Popen(["websockify", str(port),
                                                  f"localhost:{port+100}"],
                                                  stdout=subprocess.DEVNULL,
                                                  stderr=subprocess.DEVNULL))

def shutdownWebsockifys():
    for proc in websockify_procs:
        proc.terminate()
atexit.register(shutdownWebsockifys)

# Dealing with clients
def removeClient(client):
    try:
        clientSelector.unregister(client)
    except KeyError:
        pass

    client.close()

    try:
        clients.remove(client)
    except ValueError:
        pass
    try:
        del lastMessage[client]
    except KeyError:
        pass

def handleIncomingLoop():
    global clients, servers, lastMessage
    print("Starting handle incoming connections thread")
    while True:
        events = serverSelector.select()
        for key, mask in events:
            # New client
            sock = key.fileobj
            port = sock.getsockname()[1]-100
            new_client, addr = sock.accept()
            clientSelector.register(new_client, selectors.EVENT_READ)
            clients.append(new_client)
            lastMessage[new_client] = time.time()

def handleAcknowledgeLoop():
    global clients, lastMessage
    print("Starting handle acknowledge thread")
    while True:
        events = clientSelector.select()
        for key, mask in events:
            # New message from client
            sock = key.fileobj
            try:
                data = sock.recv(1024)
                if data:
                    # print(f"Received {message} from {sock.getpeername()}")
                    lastMessage[sock] = time.time()
            except OSError:
                removeClient(sock)

def handleCheckAliveLoop():
    global clients, lastMessage
    print("Starting handle check alive thread")
    while True:
        for client in clients:
            if time.time() - lastMessage[client] > 10:
                removeClient(client)
        time.sleep(10)

def wrapLoop(loopfunc):
    def wrapped():
        while True:
            try:
                loopfunc()
            except BaseException as e:
                print(f"Exception in thread {loopfunc}")
                traceback.print_exc()
            else:
                print(f"Thread {loopfunc} exited, restarting")
    return wrapped

def runBackgroundProcesses():
    handleIncomingProcess = threading.Thread(
                                        target=wrapLoop(handleIncomingLoop))
    handleAcknowledgeProcess = threading.Thread(
                                        target=wrapLoop(handleAcknowledgeLoop))
    handleCheckAliveProcess = threading.Thread(
                                        target=wrapLoop(handleCheckAliveLoop))

    handleIncomingProcess.start()
    handleAcknowledgeProcess.start()
    handleCheckAliveProcess.start()

broadcastPool = ThreadPool(32)

def broadcastToClient(client):
    global messages
    port = client.getsockname()[1]-100
    if str(port) not in messages:
        return # Selective Update
    try:
        client.send(json.dumps(messages[str(port)]).encode("utf-8"))
    except OSError:
        removeClient(client)

def broadcastToClients():
    ts = time.time()
    broadcastPool.map(broadcastToClient, clients)
    return int((time.time()-ts)*1000)

### Command Server
if enable_ssl:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_default_certs()
    context.load_cert_chain(args.cert, args.key)
    cserver_sock_unwrapped = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cserver_sock_unwrapped.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cserver_sock_unwrapped.bind(("0.0.0.0", 9100))
    cserver_sock_unwrapped.listen(16)
    cserver_sock = context.wrap_socket(cserver_sock_unwrapped, server_side=True)
else:
    cserver_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cserver_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cserver_sock.bind(("0.0.0.0", 9100))
    cserver_sock.listen(16)

class controller_type:
    SERVER = 0 # server socket
    WAITING = 1 # awaiting authentication
    CLIENT = 2 # connected client

commandServerSelector = selectors.DefaultSelector()
commandServerSelector.register(cserver_sock, selectors.EVENT_READ, controller_type.SERVER)

def removeCommandClient(client):
    commandServerSelector.unregister(client)
    try:
        client.close()
    except OSError:
        pass

def runCommandServer():
    global messages
    while True:
        events = commandServerSelector.select()

        for key, mask in events:
            client = key.fileobj
            type = key.data

            if type == controller_type.SERVER:
                # New client
                new_client, addr = cserver_sock.accept()
                if args.psk is not None:
                    commandServerSelector.register(new_client, selectors.EVENT_READ, controller_type.WAITING)
                else:
                    commandServerSelector.register(new_client, selectors.EVENT_READ, controller_type.CLIENT)

            elif type == controller_type.WAITING:
                # Client Authentication
                try:
                    data = client.recv(1024)

                except OSError: # Client is dead
                    removeCommandClient(client)
                    continue

                if len(data) == 0: # Client is disconnected
                    removeCommandClient(client)
                    continue

                msg = data.decode("utf-8", "ignore")

                if msg == args.psk:
                    commandServerSelector.modify(client, selectors.EVENT_READ, controller_type.CLIENT)
                    client.send(b"OK")
                else:
                    removeCommandClient(client)
                    continue

            elif type == controller_type.CLIENT:
                try:
                    data = client.recv(2**18)

                except OSError: # Client is dead
                    removeCommandClient(client)
                    continue

                if len(data) == 0: # Client is disconnected
                    removeCommandClient(client)
                    continue

                try:
                    obj = json.loads(data.decode("utf-8", "ignore").split("\n")[0])
                except json.JSONDecodeError:
                    removeCommandClient(client)
                    continue

                messages = obj

                latency = broadcastToClients()
                client.send(json.dumps({"clients":len(clients), "latency":latency}).encode("utf-8"))

runBackgroundProcesses()

while True:
    try:
        runCommandServer()
    except Exception as e:
        print("Error in Command Server:")
        traceback.print_exc()
