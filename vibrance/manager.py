import os
import sys
import importlib
import importlib.util

from . import controller


class Manager:
    def __init__(self):
        self.ctrl = controller.Controller()
        self.inputs = {}
        self.inputTypes = {}
        self.scripts = {}
        self.input = None
        self.script = None

    def connect(self, host, psk=None):
        self.ctrl.connect(host, psk)

    def addInput(self, input):
        self.inputs[input.name] = input

    def addInputFile(self, path):
        specname = f"manager_input_{len(self.inputs)}"

        spec = importlib.util.spec_from_file_location(specname, path)
        input = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = input
        spec.loader.exec_module(input)

        if not input.input.name:
            input.input.name = specname

        self.inputs[input.input.name] = input.input

    def addScript(self, path):
        specname = f"manager_script_{len(self.scripts)}"

        spec = importlib.util.spec_from_file_location(specname, path)
        script = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = script
        spec.loader.exec_module(script)

        if not script.api.name:
            script.api.name = specname

        self.scripts[script.api.name] = script.api

    def configure(self, path=None):
        self.addInputsFromDirectory(os.path.join(path, "inputs"))
        self.addScriptsFromDirectory(os.path.join(path, "scripts"))

    def addInputsFromDirectory(self, path):
        files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".py")]
        for file in files:
            self.addInputFile(file)

    def addScriptsFromDirectory(self, path):
        files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".py")]
        for file in files:
            self.addScript(file)

    def chooseInput(self, input):
        if self.input:
            self.input.close()
        self.input = input
        self.input.open()

    def chooseScript(self, script):
        self.script = script

    def getStatus(self):
        return {}

    def handle(self):
        self.script.handle(self.input, self.ctrl)

    def run(self):
        while True:
            self.handle()

if __name__ == "__main__":
    # Run this module directly for a CLI manager

    manager = Manager()
    manager.connect(sys.argv[1], sys.argv[2])
    manager.configure(sys.argv[3])

    def promptInput():
        print("Select input:")
        for name in manager.inputs.keys():
            print(name)
        manager.chooseInput(manager.inputs[input("> ")])

    def promptScript():
        print("Select script:")
        for name in manager.scripts.keys():
            print(name)
        manager.chooseScript(manager.scripts[input("> ")])

    promptInput()
    promptScript()

    while True:
        try:
            manager.run()
        except KeyboardInterrupt:
            try:
                promptScript()
            except KeyboardInterrupt:
                promptInput()
                promptScript()
