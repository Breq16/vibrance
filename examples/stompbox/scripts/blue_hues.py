import math
import time

import vibrance

api = vibrance.Interface("Blue Hues")

MODE = 0
RADIANS = 0
FRAME = 0

def getColor(radians):
    red = max(0, int(0xFF * math.sin(radians + math.pi)))
    green = max(0, int(0xFF * math.sin(radians)))
    blue = 0xFF
    return f"{format(red, '02x')}{format(green, '02x')}{format(blue, '02x')}"

@api.on("uart", "d")
def down(event):
    global MODE
    MODE += 1
    if MODE > 1:
        MODE = 0
    lastUpdate = 0 # trigger an update immediately

lastUpdate = 0

PALETTE = ("0000FF", "FF00FF", "00FFFF")

@api.loop
def loop():
    global MODE, RADIANS, FRAME, lastUpdate

    if (time.time() - lastUpdate) < 0.5:
        return
    lastUpdate = time.time()

    if MODE == 0:
        for i in range(5):
            RADIANS += 0.1
            api.color((0, 2), getColor(RADIANS))
            api.color((1, 3), getColor(RADIANS+math.pi))
            api.wait(0.1)
    elif MODE == 1:
        FRAME += 1
        for zone in (0, 1, 2, 3):
            api.color(zone, PALETTE[(FRAME+zone) % 3])
            api.wait(0.125)
