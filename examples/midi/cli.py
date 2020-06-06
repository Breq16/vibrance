import importlib
import threading
import sys

import vibrance
import vibrance.input.midi

module_names = ["simple", "animations"]

ctrl = vibrance.Controller()
ctrl.connect(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

mdin = vibrance.input.midi.MidiInput("vibrance")

modules = {}
for name in module_names:
    modules[name] = importlib.import_module(name)

def run_module(name):
    try:
        modules[name].api.run(mdin, ctrl)
    except KeyboardInterrupt:
        return

while True:
    print("Loaded modules:")
    for name in modules.keys():
        print(name)
    name = input("> ")
    if name not in modules:
        print("Choose a module")
        continue

    run_module(name)
