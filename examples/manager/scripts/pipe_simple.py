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

api = vibrance.Interface("Broken Pipe") # haha, because it's the pipe input demo, and it's kinda broken...

@api.on("pipe", "cycle")
def cycle(event):
    i = event["color"]

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
    api.color((0, 1, 3, 4), "000")

@api.on("pipe", "chase")
def chase(event):
    i = event["color"]

    for zone in (2, 1, 0, 3, 4, 5):
        api.color(zone, PALETTE[i])
        api.color([z for z in ZONES if z != zone], "000")
        api.wait(0.1)

@api.on("pipe", "clear")
def clear(event):
    api.color(ZONES, "000")

@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)
