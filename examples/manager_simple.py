import sys

import vibrance

manager = vibrance.Manager()

manager.connect(sys.argv[1], sys.argv[2])

manager.configure("manager")

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
