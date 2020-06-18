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

api = vibrance.Interface("QWERTY Animations")

CYCLE_KEYS = ("q", "w", "e", "r", "t", "y", "u")
CHASE_KEYS = ("a", "s", "d", "f", "g", "h", "j")
EXPAND_KEYS = ("z", "x", "c", "v", "b", "n", "m")

BPM = 122 / 2

BEAT_TIME = 60 / BPM

@api.on("pygame", "keydown")
def keydown(event):
    key = event["key"]
    if key == ord(" "):
        clear()
    elif chr(key) in CYCLE_KEYS:
        i = 1 + CYCLE_KEYS.index(chr(key))
        cycle(i)
    elif chr(key) in CHASE_KEYS:
        i = 1 + CHASE_KEYS.index(chr(key))
        chase(i)
    elif chr(key) in EXPAND_KEYS:
        i = 1 + EXPAND_KEYS.index(chr(key))
        expand(i)


def cycle(i):
    api.color((0, 3), PALETTE[i])
    api.color((1, 2, 4, 5), "000")
    api.wait(BEAT_TIME / 8)

    api.color((1, 4), PALETTE[i])
    api.color((0, 2, 3, 5), "000")
    api.wait(BEAT_TIME / 8)

    api.color((2, 5), PALETTE[i])
    api.color((0, 1, 3, 4), "000")
    api.wait(BEAT_TIME / 8)

    api.color((1, 4), PALETTE[i])
    api.color((0, 2, 3, 5), "000")


def expand(i):
    api.color(1, PALETTE[i])
    api.color((0, 2, 3, 4, 5), "000")
    api.wait(BEAT_TIME / 8)

    api.color((0, 2, 4), PALETTE[i])
    api.color((1, 3, 5), "000")
    api.wait(BEAT_TIME / 8)

    api.color((3, 5), PALETTE[i])
    api.color((0, 1, 2, 4), "000")
    api.wait(BEAT_TIME / 8)

    api.color((0, 1, 2, 3, 4, 5), "000")


def chase(i):
    for zone in (2, 1, 0, 3, 4, 5):
        api.color(zone, PALETTE[i])
        api.color([z for z in ZONES if z != zone], "000")
        api.wait(BEAT_TIME / 12)


def clear():
    api.color(ZONES, "000")


@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)
