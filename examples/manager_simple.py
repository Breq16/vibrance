import sys

import vibrance

manager = vibrance.Manager()

manager.connect(sys.argv[1], sys.argv[2])

import vibrance.input.midi
import vibrance.input.pygame_if

manager.addInput(vibrance.input.midi.MidiInput(), "MIDI")
manager.addInput(vibrance.input.pygame_if.PyGameInput(), "PyGame")

manager.addScript("midi/simple.py", "MIDI Simple")
manager.addScript("midi/animations.py", "MIDI Animations")
manager.addScript("pygame_simple.py", "PyGame Simple")

while True:
    print("Select input:")
    for name in manager.inputs.keys():
        print(name)
    manager.chooseInput(manager.inputs[input("> ")])

    print("Select script:")
    for name in manager.scripts.keys():
        print(name)
    manager.chooseScript(manager.scripts[input("> ")])

    try:
        manager.run()
    except KeyboardInterrupt:
        pass
