import importlib
import threading

import controller
import midi

module_names = ["simple", "animations"]

ctrl = controller.Controller()
ctrl.connect("cloud.itsw.es")

mdin = midi.MidiInput()

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
