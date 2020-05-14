import controller
import json
import readline
import os
import sys
import atexit

histfile = os.path.join(os.path.expanduser("~"), ".vibrance_history")

try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)

if len(sys.argv) < 2:
    print("Usage: message_composer.py [relay address]")
    sys.exit()

ctrl = controller.Controller(sys.argv[1])

while True:
    i = input("Messages> ")
    ctrl.clear()
    ctrl.messages = json.loads(i)
    print(ctrl.write())
