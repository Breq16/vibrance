import math
import time

import vibrance

api = vibrance.Interface("Fading and Flashing")

MODE = 0
RADIANS = 0
FRAME = 0

UPDATE_INTERVAL = 2
BPM = 122
BEAT_TIME = 60 / BPM

PALETTE = ("FF8000", "00FF00", "FFFFFF")


def getFadingColor(radians):
    red = max(0, int(0xFF * math.sin(radians + math.pi)))
    green = max(0, int(0xFF * math.sin(radians)))
    blue = 0xFF
    return f"{format(red, '02x')}{format(green, '02x')}{format(blue, '02x')}"

def getFlashingColor(frame):
    return PALETTE[frame % len(PALETTE)]

@api.on("uart", "d")
def down(event):
    global MODE, lastUpdate
    MODE += 1
    if MODE > 1:
        MODE = 0
    lastUpdate = 0  # trigger an update immediately


lastUpdate = 0


@api.loop
def loop():
    global MODE, RADIANS, FRAME, lastUpdate, UPDATE_INTERVAL

    if (time.time() - lastUpdate) < (BEAT_TIME/4)*UPDATE_INTERVAL:
        return
    lastUpdate = time.time()

    for i in range(UPDATE_INTERVAL):
        if MODE == 0:
            RADIANS += 0.1
            api.color((0, 2), getFadingColor(RADIANS))
            api.color((1, 3), getFadingColor(RADIANS+math.pi))
            api.wait(BEAT_TIME / 4)
        elif MODE == 1:
            api.color((FRAME % 4), getFlashingColor(FRAME))
            api.color([z for z in range(4) if z != (FRAME % 4)], "000")
            FRAME += 1
            api.wait(BEAT_TIME / 4)
