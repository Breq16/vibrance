import colorsys
import os

import mido

# Find Vibrance Port
if os.name == "posix":
    # macOS or Linux systems
    # Just create a virtual port
    outport = mido.open_output("vibrance")
elif os.name == "nt":
    # Windows system
    # Rely on external MIDI loopback software
    outport = mido.open_output("vibrance_loopback 4")
else:
    raise ValueError("unsupported OS")

try:
    while True:
        note = int(input("Note> "))
        velocity = int(input("Vel> "))

        msg = mido.Message("note_on")
        msg.note = note
        msg.velocity = velocity

        if outport.closed:
            break

        outport.send(msg)
finally:
    outport.close()
