import json
import readline
import os
import sys
import atexit

import vibrance

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

api = vibrance.Interface()

ctrl = vibrance.Controller()
ctrl.connect(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)

while True:
    i = input("Messages> ")
    api.clear()
    api.messages = json.loads(i)
    api.update(ctrl)
