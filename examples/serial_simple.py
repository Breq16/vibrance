import vibrance
import vibrance.uart

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

api = vibrance.uart.SerialInterface()

@api.onByte(b"a")
def a(byte):
    api.color(9001, "FF0")
    api.color((9002, 9003), "000")
    api.wait(1)
    api.color(9002, "FF0")
    api.color((9001, 9003), "000")
    api.wait(1)
    api.color(9003, "FF0")
    api.color((9001, 9002), "000")

@api.onByte(b"b")
def b(byte):
    api.color(9004, "FF0")
    api.color((9005, 9006), "000")
    api.wait(1)
    api.color(9005, "FF0")
    api.color((9004, 9006), "000")
    api.wait(1)
    api.color(9006, "FF0")
    api.color((9004, 9005), "000")

@api.onAny
def any(byte):
    i = int.from_bytes(byte, "little")
    if 0 <= i < len(PALETTE):
        api.color(range(9001, 9007), PALETTE[i])

@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)

if __name__ == "__main__":
    import sys

    ctrl = vibrance.Controller()
    ctrl.connect(sys.argv[1], sys.argv[2])

    uart = vibrance.uart.SerialInput(sys.argv[3])

    api.run(uart, ctrl)
