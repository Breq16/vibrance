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

color = PALETTE[0]

enabled = {zone: False for zone in range(6)}

api = vibrance.Interface("Keypad Simple")

def recompute():
    global color, enabled
    for zone in enabled:
        if enabled[zone]:
            api.color(zone, color)
        else:
            api.color(zone, "000")

@api.on("keypad", "letter")
def onLetter(event):
    key = event["key"]
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

@api.on("keypad", "number")
def onNumber(event):
    key = event["key"]
    global enabled
    for zone in enabled:
        enabled[zone] = False
    if key == "1":
        enabled[0] = True
        enabled[3] = True
    elif key == "2":
        enabled[1] = True
        enabled[4] = True
    elif key == "3":
        enabled[2] = True
        enabled[5] = True
    elif key == "4":
        enabled[3] = True
    elif key == "5":
        enabled[4] = True
    elif key == "6":
        enabled[5] = True
    elif key == "7":
        enabled[0] = True
    elif key == "8":
        enabled[1] = True
    elif key == "9":
        enabled[2] = True
    elif key == "0":
        enabled[0] = True
        enabled[1] = True
        enabled[2] = True
        enabled[3] = True
        enabled[4] = True
        enabled[5] = True
    recompute()
