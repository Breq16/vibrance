import socket
import select
import subprocess
import atexit
import time
import json
import threading
import traceback
import ssl
import os
import pathlib
from multiprocessing.dummy import Pool as ThreadPool

psk = (pathlib.Path(__file__).parent / "secrets/psk.txt").resolve()
cert = (pathlib.Path(__file__).parent / "secrets/fullchain.pem").resolve()
key  = (pathlib.Path(__file__).parent / "secrets/privkey.pem").resolve()

enable_ssl = True

ports = list(range(9001, 9007))
messages = {}
servers = []
clients = []
lastMessage = {}
websockify_procs = []

for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", port+100))
    sock.listen(16)
    servers.append(sock)

for port in ports:
    # Start the websockify
    if enable_ssl:
        websockify_procs.append(subprocess.Popen(["websockify", str(port),
                                                  f"localhost:{port+100}",
                                                  f"--cert={cert}",
                                                  f"--key={key}"]))
    else:
        websockify_procs.append(subprocess.Popen(["websockify", str(port),
                                                  f"localhost:{port+100}"]))

def shutdownWebsockifys():
    for proc in websockify_procs:
        proc.terminate()
atexit.register(shutdownWebsockifys)

# Dealing with clients
def removeClient(client):
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
        read_servers = select.select(servers, [], [], 0)[0]
        for sock in read_servers:
            # New client
            port = sock.getsockname()[1]-100
            new_client, addr = sock.accept()
            clients.append(new_client)
            lastMessage[new_client] = time.time()
            print(f"New client from {addr} on port {port}")

def handleAcknowledgeLoop():
    global clients, lastMessage
    print("Starting handle acknowledge thread")
    while True:
        try:
            read_clients = select.select(clients, [], [], 0)[0]
        except OSError:
            continue
        for sock in read_clients:
            # New message from client
            try:
                data = sock.recv(1024)
                if data:
                    # print(f"Received {message} from {sock.getpeername()}")
                    lastMessage[sock] = time.time()
            except OSError:
                print("Error receiving message, terminating client")
                removeClient(sock)

def handleCheckAliveLoop():
    global clients, lastMessage
    print("Starting handle check alive thread")
    while True:
        for client in clients:
            if time.time() - lastMessage[client] > 10:
                removeClient(client)
                try:
                    print(f"Terminating dead client {client.getpeername()}")
                except:
                    print("Terminating dead client")
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
    except Exception as e:
        print(f"Failed send to {port} client")
        traceback.print_exc()
        removeClient(client)

def broadcastToClients():
    ts = time.time()
    broadcastPool.map(broadcastToClient, clients)
    return int((time.time()-ts)*1000)

### Command Server
if enable_ssl:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_default_certs()
    context.load_cert_chain(cert, key)
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

cclients = []
cclients_awaiting_auth = []

if os.path.exists("secrets/psk.txt"):
    with open("secrets/psk.txt") as f:
        PASSWORD = f.read().rstrip("\r\n")
else:
    print("Warning: No password set")
    print("Create the file ./secrets/psk.txt")
    print("with the password for the controller interface")
    print("(not doing this allows anyone to use this)")
    print("Using default password `password`...")

def runCommandServer():
    global messages
    while True:
        # New Clients
        read_server = select.select([cserver_sock], [], [], 0)[0]
        if cserver_sock in read_server:
            new_client, addr = cserver_sock.accept()
            cclients_awaiting_auth.append(new_client)
            print(f"New command client from {addr} awaiting authentication")

        # Client Authentication
        read_clients_awaiting = select.select(cclients_awaiting_auth, [], [], 0)[0]
        for client in read_clients_awaiting:
            print("New data from client awaiting auth")
            try:
                data = client.recv(2**18)
                if len(data) == 0:
                    print("Socket closed")
                    cclients_awaiting_auth.remove(client)
                    try:
                        client.close()
                    except Exception:
                        pass
                    continue
            except Exception as e:
                print("Error reading")
                traceback.print_exc()
                cclients_awaiting_auth.remove(client)
                try:
                    client.close()
                except Exception:
                    pass
                continue
            try:
                message = data.decode()
            except Exception:
                print("Unable to decode message")
            else:
                if message == PASSWORD:
                    print("Client authenticated")
                    cclients.append(client)
                    cclients_awaiting_auth.remove(client)
                    client.send(b"OK")
                else:
                    print("Authentication failed")
                    cclients_awaiting_auth.remove(client)
                    try:
                        client.close()
                    except Exception:
                        pass

        # Authenticated Clients
        read_clients = select.select(cclients, [], [], 0)[0]
        for client in read_clients:
            print("New data")
            try:
                data = client.recv(2**18)
                if len(data) == 0:
                    print("Socket closed")
                    cclients.remove(client)
                    try:
                        client.close()
                    except Exception:
                        pass
                    continue
            except Exception as e:
                print("Error reading from command client, removing")
                traceback.print_exc()
                cclients.remove(client)
                try:
                    client.close()
                except Exception:
                    pass
                continue
            try:
                line = data.decode().split("\n")[0]
                messages = json.loads(line)
            except Exception as e:
                print("Unable to decode message")
                traceback.print_exc()
            else:
                print(messages)
                latency = broadcastToClients()
                client.send(json.dumps({"clients":len(clients), "latency":latency}).encode("utf-8"))



runBackgroundProcesses()

while True:
    try:
        runCommandServer()
    except Exception as e:
        print("Error in Command Server:")
        traceback.print_exc()
