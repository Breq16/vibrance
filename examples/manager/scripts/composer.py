import os
import readline
import atexit
import json

import vibrance

histfile = os.path.join(os.path.expanduser("~"), ".vibrance_history")

try:
    readline.read_history_file(histfile)
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)

api = vibrance.Interface("Terminal Composer")

@api.loop
def loop():
    i = input("Messages> ")
    api.messages = json.loads(i)
