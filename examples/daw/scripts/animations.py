import vibrance

PALETTE = (
    "000000",  # black
    "FFFFFF",  # white
    "FF0000",  # red
    "00FF00",  # green
    "0000FF",  # blue
    "FFFF00",  # yellow
    "00FFFF",  # cyan
    "FF00FF",  # magenta
    "FF8000",  # orange
    "8000FF",  # purple
    "0080FF",  # light blue
    "FF0080",  # pink
)

ZONES = list(range(6))

api = vibrance.Interface("Octave Animations")

BPM = 122 / 2

BEAT_TIME = 60 / BPM


@api.on("midi", "note_on_oct_-2")
def cycle(event):
    i = event["note"] % 12

    api.color((0, 3), PALETTE[i])
    api.color((1, 2, 4, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color((1, 4), PALETTE[i])
    api.color((0, 2, 3, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color((2, 5), PALETTE[i])
    api.color((0, 1, 3, 4), "000")
    api.wait(BEAT_TIME / 2)

    api.color((1, 4), PALETTE[i])
    api.color((0, 2, 3, 5), "000")


@api.on("midi", "note_on_oct_-1")
def expand(event):
    i = event["note"] % 12

    api.add(1, PALETTE[i])
    api.color((0, 2, 3, 4, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color((0, 2, 4), PALETTE[i])
    api.color((1, 3, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color((3, 5), PALETTE[i])
    api.color((0, 1, 2, 4), "000")
    api.wait(BEAT_TIME / 2)

    api.color((0, 1, 2, 3, 4, 5), "000")


@api.on("midi", "note_on_oct_0")
def chase(event):
    i = event["note"] % 12
    for zone in (2, 1, 0, 3, 4, 5):
        api.color(zone, PALETTE[i])
        api.color([z for z in ZONES if z != zone], "000")
        api.wait(BEAT_TIME / 3)


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
        api.wait(BEAT_TIME / 4)


@api.on("midi", "note_on_oct_2")
def across_from_front_left(event):
    i = event["note"] % 12

    api.add(0, PALETTE[i])
    api.color((1, 2, 3, 4, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color((1, 3), PALETTE[i])
    api.color((0, 2, 4, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color((2, 4), PALETTE[i])
    api.color((0, 1, 3, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color(5, PALETTE[i])
    api.color((0, 1, 2, 3, 4), "000")


@api.on("midi", "note_on_oct_3")
def across_from_front_right(event):
    i = event["note"] % 12

    api.add(2, PALETTE[i])
    api.color((1, 0, 3, 4, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color((1, 5), PALETTE[i])
    api.color((0, 2, 4, 3), "000")
    api.wait(BEAT_TIME / 2)

    api.color((0, 4), PALETTE[i])
    api.color((2, 1, 3, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color(3, PALETTE[i])
    api.color((0, 1, 2, 5, 4), "000")


@api.on("midi", "note_on_oct_4")
def across_from_back_left(event):
    i = event["note"] % 12

    api.add(3, PALETTE[i])
    api.color((1, 2, 0, 4, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color((0, 4), PALETTE[i])
    api.color((1, 2, 3, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color((1, 5), PALETTE[i])
    api.color((0, 2, 3, 4), "000")
    api.wait(BEAT_TIME / 2)

    api.color(2, PALETTE[i])
    api.color((0, 1, 5, 3, 4), "000")


@api.on("midi", "note_on_oct_5")
def across_from_back_right(event):
    i = event["note"] % 12

    api.add(5, PALETTE[i])
    api.color((1, 0, 3, 4, 2), "000")
    api.wait(BEAT_TIME / 2)

    api.color((2, 4), PALETTE[i])
    api.color((0, 1, 5, 3), "000")
    api.wait(BEAT_TIME / 2)

    api.color((1, 3), PALETTE[i])
    api.color((2, 0, 4, 5), "000")
    api.wait(BEAT_TIME / 2)

    api.color(0, PALETTE[i])
    api.color((3, 1, 2, 5, 4), "000")


@api.on("midi", "note_on_127")
def clear(event):
    api.color(ZONES, "000")


@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)
