import os
import sys
import importlib
import importlib.util

from . import controller
from . import interface
from .driver import base


class Manager:
    def __init__(self):
        self.ctrl = controller.Controller()
        self.drivers = {"None": base.BaseDriver("None")}
        self.scripts = {"None": interface.Interface("None")}
        self.driver = self.drivers["None"]
        self.script = self.scripts["None"]

    def connect(self, host, psk=None):
        self.ctrl.connect(host, psk)

    def addDriver(self, driver):
        self.drivers[driver.name] = driver

    def addDriverFile(self, path):
        specname = f"manager_driver_{len(self.drivers)}"

        spec = importlib.util.spec_from_file_location(specname, path)
        driver_module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = driver_module
        spec.loader.exec_module(driver_module)

        if not driver_module.driver.name:
            driver_module.driver.name = specname

        self.drivers[driver_module.driver.name] = driver_module.driver

    def addScript(self, path):
        specname = f"manager_script_{len(self.scripts)}"

        spec = importlib.util.spec_from_file_location(specname, path)
        script = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = script
        spec.loader.exec_module(script)

        if not script.api.name:
            script.api.name = specname

        self.scripts[script.api.name] = script.api

    def configure(self, path):
        self.addDriversFromDirectory(os.path.join(path, "drivers"))
        self.addScriptsFromDirectory(os.path.join(path, "scripts"))

    def addDriversFromDirectory(self, path):
        files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".py")]
        for file in files:
            self.addDriverFile(file)

    def addScriptsFromDirectory(self, path):
        files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".py")]
        for file in files:
            self.addScript(file)

    def chooseDriver(self, driver):
        if self.driver:
            self.driver.close()
        self.driver = driver
        self.driver.open()

    def chooseScript(self, script):
        self.script = script

    def getStatus(self):
        return {}

    def handle(self):
        if self.script:
            self.script.handle(self.driver, self.ctrl)

    def run(self):
        while True:
            self.handle()

if __name__ == "__main__":
    # Run this module directly for a CLI manager

    manager = Manager()
    manager.connect(sys.argv[1], sys.argv[2])
    manager.configure(sys.argv[3])

    def promptDriver():
        print("Select driver:")
        for name in manager.drivers.keys():
            print(name)
        manager.chooseDriver(manager.drivers[input("> ")])

    def promptScript():
        print("Select script:")
        for name in manager.scripts.keys():
            print(name)
        manager.chooseScript(manager.scripts[input("> ")])

    promptDriver()
    promptScript()

    while True:
        try:
            manager.run()
        except KeyboardInterrupt:
            try:
                promptScript()
            except KeyboardInterrupt:
                promptDriver()
                promptScript()
