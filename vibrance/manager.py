import sys
import importlib.util

from . import controller


class Manager:
    def __init__(self):
        self.ctrl = controller.Controller()
        self.inputs = {}
        self.scripts = {}
        self.input = None
        self.script = None

    def connect(self, host, psk=None):
        self.ctrl.connect(host, psk)

    def addInput(self, input, name):
        self.inputs[name] = input

    def addScript(self, path, name=None):
        if name is None:
            name = path

        specname = f"manager_script_{len(self.scripts)}"

        spec = importlib.util.spec_from_file_location(specname, path)
        script = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = script
        spec.loader.exec_module(script)

        self.scripts[name] = script

    def chooseInput(self, input):
        self.input = input

    def chooseScript(self, script):
        self.script = script

    def handle(self):
        self.script.api.handle(self.input, self.ctrl)

    def run(self):
        while True:
            self.handle()
