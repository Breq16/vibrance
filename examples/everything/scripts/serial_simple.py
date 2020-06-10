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

api = vibrance.Interface("Arduino Example")


@api.on("uart", "a")
def a(event):
    api.color(0, "FF0")
    api.color((1, 2), "000")
    api.wait(1)
    api.color(1, "FF0")
    api.color((0, 2), "000")
    api.wait(1)
    api.color(2, "FF0")
    api.color((0, 1), "000")


@api.on("uart", "b")
def b(event):
    api.color(3, "FF0")
    api.color((4, 5), "000")
    api.wait(1)
    api.color(4, "FF0")
    api.color((3, 5), "000")
    api.wait(1)
    api.color(5, "FF0")
    api.color((3, 4), "000")


@api.on("uart", "byte")
def any(event):
    i = int.from_bytes(event["byte"], "little")
    if 0 <= i < len(PALETTE):
        api.color(range(6), PALETTE[i])


@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)
