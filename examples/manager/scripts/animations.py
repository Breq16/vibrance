import vibrance

PALETTE = (
    "000000", # black
    "FFFFFF", # white
    "FF0000", # red
    "00FF00", # green
    "0000FF", # blue
    "FFFF00", # yellow
    "00FFFF", # cyan
    "FF00FF", # magenta
    "FF8000", # orange
    "8000FF", # purple
    "0080FF", # light blue
    "FF0080", # pink
)

ZONES = list(range(6))

api = vibrance.Interface("MIDI Animations")

@api.on("midi", "note_on_oct_-2")
def cycle(event):
    i = event["note"] % 12

    api.color((0, 3), PALETTE[i])
    api.color((1, 2, 4, 5), "000")
    api.wait(0.5)

    api.color((1, 4), PALETTE[i])
    api.color((0, 2, 3, 5), "000")
    api.wait(0.5)

    api.color((2, 5), PALETTE[i])
    api.color((0, 1, 3, 4), "000")
    api.wait(0.5)

    api.color((1, 4), PALETTE[i])
    api.color((0, 2, 3, 5), "000")

@api.on("midi", "note_on_oct_-1")
def expand(event):
    i = event["note"] % 12

    api.add(1, PALETTE[i])
    api.color((0, 2, 3, 4, 5), "000")
    api.wait(0.5)

    api.color((0, 2, 4), PALETTE[i])
    api.color((1, 3, 5), "000")
    api.wait(0.5)

    api.color((3, 5), PALETTE[i])
    api.color((0, 1, 2, 4), "000")

@api.on("midi", "note_on_oct_0")
def chase(event):
    i = event["note"] % 12
    for zone in (2, 1, 0, 3, 4, 5):
        api.color(zone, PALETTE[i])
        api.color([z for z in ZONES if z != zone], "000")
        api.wait(0.1)

@api.on("midi", "note_on_oct_1")
def back_and_forth(event):
    i = event["note"] % 12
    for j in range(8):
        if j % 2 == 0:
            api.color((0, 1, 2), PALETTE[i])
            api.color((3, 4, 5), "000")
        else:
            api.color((3, 4, 5), PALETTE[i])
            api.color((0, 1, 2), "000")
        api.wait(0.2)


@api.on("midi", "note_on_127")
def clear(event):
    api.color(ZONES, "000")

@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)

if __name__ == "__main__":
    import sys
    import vibrance.input.midi

    ctrl = vibrance.Controller()
    ctrl.connect(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

    min = vibrance.input.midi.MidiInput("vibrance")

    api.run(min, ctrl)
