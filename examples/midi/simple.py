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

ZONEMAP = (
    (1, 0, 0, 0, 0, 0), # oct -2
    (0, 1, 0, 0, 0, 0), # oct -1
    (0, 0, 1, 0, 0, 0), # oct 0
    (0, 0, 0, 1, 0, 0), # oct 1
    (0, 0, 0, 0, 1, 0), # oct 2
    (0, 0, 0, 0, 0, 1), # oct 3
    (1, 1, 1, 1, 1, 1), # oct 4
    (1, 0, 0, 1, 0, 0), # oct 5
    (0, 1, 0, 0, 1, 0), # oct 6
    (0, 0, 1, 0, 0, 1), # oct 7
)

api = vibrance.Interface()

@api.on("midi", "note_on")
def test(event):
    print(event)
    if event["type"] == "note_on":
        octNote = event["note"] % 12
        octave = event["note"] // 12

        if octave > 9:
            return # Reserved for future use

        color = PALETTE[octNote]
        zones = ZONEMAP[octave]

        for i, zone in enumerate(zones):
            if zone:
                api.add(i, color)
            elif event["velocity"] > 75:
                api.add(i, "000000")

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
