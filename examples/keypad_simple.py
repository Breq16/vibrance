import vibrance
import vibrance.keypad

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

color = PALETTE[0]

enabled = {port: False for port in range(9001, 9007)}

api = vibrance.keypad.KeypadInterface()

def recompute():
    global color, enabled
    for zone in enabled:
        if enabled[zone]:
            api.color(zone, color)
        else:
            api.color(zone, "000")

@api.onLetter
def onLetter(key):
    global color
    if key == "q":
        color = PALETTE[0]
    elif key == "w":
        color = PALETTE[1]
    elif key == "e":
        color = PALETTE[2]
    elif key == "r":
        color = PALETTE[3]
    elif key == "a":
        color = PALETTE[4]
    elif key == "s":
        color = PALETTE[5]
    elif key == "d":
        color = PALETTE[6]
    elif key == "f":
        color = PALETTE[7]
    elif key == "z":
        color = PALETTE[8]
    elif key == "x":
        color = PALETTE[9]
    elif key == "c":
        color = PALETTE[10]
    elif key == "v":
        color = PALETTE[11]
    recompute()

@api.onNumber
def onNumber(key):
    global enabled
    for zone in enabled:
        enabled[zone] = False
    if key == "1":
        enabled[9001] = True
        enabled[9004] = True
    elif key == "2":
        enabled[9002] = True
        enabled[9005] = True
    elif key == "3":
        enabled[9003] = True
        enabled[9006] = True
    elif key == "4":
        enabled[9004] = True
    elif key == "5":
        enabled[9005] = True
    elif key == "6":
        enabled[9006] = True
    elif key == "7":
        enabled[9001] = True
    elif key == "8":
        enabled[9002] = True
    elif key == "9":
        enabled[9003] = True
    elif key == "0":
        enabled[9001] = True
        enabled[9002] = True
        enabled[9003] = True
        enabled[9004] = True
        enabled[9005] = True
        enabled[9006] = True
    recompute()

@api.onTelemetry
def onTelemetry(telemetry):
    #print(telemetry)
    pass

if __name__ == "__main__":
    import sys

    ctrl = vibrance.Controller()
    ctrl.connect(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

    keypad = vibrance.keypad.KeypadInput()

    api.run(keypad, ctrl)
