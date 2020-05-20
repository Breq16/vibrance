import socket
import subprocess
import atexit
import time
import json
import threading
import traceback
import ssl
import os
import selectors
import argparse
import tempfile
from multiprocessing.dummy import Pool as ThreadPool

from . import appserver, controlserver

parser = argparse.ArgumentParser(description="Run a Vibrance relay server "
                                 "(command server and client WebSocket "
                                 "servers).")

parser.add_argument("--psk", help="Optional password for the command server.")

parser.add_argument("--cert", help="SSL certificate for securing the "
                    "WebSockets and the command server.")

parser.add_argument("--key", help="SSL private key for securing the WebSockets"
                    " and the command server.")

args = parser.parse_args()

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


appServer = appserver.AppServer(args.cert, args.key)
controlServer = controlserver.ControlServer(appServer, args.psk,
                                    args.cert, args.key)

appServerThread = threading.Thread(
    target=wrapLoop(appServer.run))
controlServerThread = threading.Thread(
    target=wrapLoop(controlServer.run))
appCheckAliveThread = threading.Thread(
    target=wrapLoop(appServer.handleCheckAlive))

appServerThread.start()
controlServerThread.start()
appCheckAliveThread.start()

while True:
    time.sleep(1)
