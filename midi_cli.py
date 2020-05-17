import controller
import midi
import midi_input

import importlib
import threading

module_names = ["midi_simple", "midi_animations"]

ctrl = controller.Controller()
ctrl.connect("cloud.itsw.es")

mdin = midi_input.MidiInput()

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
