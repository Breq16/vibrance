import math
import time
import sys

import vibrance

api = vibrance.Interface()

def getColor(radians):
    red = 0x80 + int(0x79*math.sin(radians))
    green = 0x80 + int(0x79*math.sin(radians+math.pi*2/3))
    blue = 0x80 + int(0x79*math.sin(radians+math.pi*4/3))
    return f"{format(red, '02x')}{format(green, '02x')}{format(blue, '02x')}"

@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)

frame = 0

def mainloop(ctrl):
    global frame
    api.clear()
    for i in range(20):
        api.add(9001, getColor(frame/50), delay=i*50)
        api.add(9002, getColor(frame/50+math.pi*1/3), delay=i*50)
        api.add(9003, getColor(frame/50+math.pi*2/3), delay=i*50)
        api.add(9004, getColor(frame/50+math.pi), delay=i*50)
        api.add(9005, getColor(frame/50+math.pi*4/3), delay=i*50)
        api.add(9006, getColor(frame/50+math.pi*5/3), delay=i*50)
        frame += 1
    ts = time.time()
    api.update(ctrl)
    time.sleep(1 + ts - time.time())

if __name__ == "__main__":
    import sys

    ctrl = vibrance.Controller()
    ctrl.connect(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

    while True:
        mainloop(ctrl)
