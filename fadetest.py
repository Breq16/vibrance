import controller
import math
import time

ctrl = controller.Controller("cloud.itsw.es")

def getColor(radians):
    red = 0x80 + int(0x79*math.sin(radians))
    green = 0x80 + int(0x79*math.sin(radians+math.pi*2/3))
    blue = 0x80 + int(0x79*math.sin(radians+math.pi*4/3))
    return f"{format(red, '02x')}{format(green, '02x')}{format(blue, '02x')}"

frame = 0
while True:
    ctrl.clear()
    for i in range(20):
        ctrl.add(9001, getColor(frame/50), delay=i*50)
        ctrl.add(9002, getColor(frame/50+math.pi*1/3), delay=i*50)
        ctrl.add(9003, getColor(frame/50+math.pi*2/3), delay=i*50)
        ctrl.add(9004, getColor(frame/50+math.pi), delay=i*50)
        ctrl.add(9005, getColor(frame/50+math.pi*4/3), delay=i*50)
        ctrl.add(9006, getColor(frame/50+math.pi*5/3), delay=i*50)
        frame += 1
    ts = time.time()
    print("Sending update... ")
    print(len(str(ctrl.messages)))
    print(ctrl.write())
    time.sleep(1 + ts - time.time())
