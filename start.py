#!/usr/bin/env micropython
from main import Menu, Move, Util
menu = Menu()
move = Move()
util = Util()
import time, os


def CalibrateColor():
    dataL = []
    dataR = []
    tic = time.perf_counter()
    while time.perf_counter() < tic + 4:
        os.system("clear")
        print("calibrating")
        dataL.append(move.colorSensorLeft.reflected_light_intensity)
        dataR.append(move.colorSensorRight.reflected_light_intensity)
    
    leftAvg = move.Avg(min(dataL), max(dataL))
    rightAvg = move.Avg(min(dataR), max(dataR))
    final = move.Avg(rightAvg, leftAvg)
    print(final)
    time.sleep(3)
    return final

    

stop = False
default = 1
menu.console.set_font("Lat15-Terminus32x16.psf.gz", True)
menu.time.sleep(2)
selected = 1
print("Ready for sensor calibration?")
while True:
    if menu.button.enter:
        break
os.system("clear")

menu.settarget(CalibrateColor())
while True:
    try:
        while True:
            selected = menu.selection(default)
            if selected == None:
                continue
            isdone = menu.run(selected)
            #menu.time.sleep(1)
            if isdone == "end":
                stop = True
                break
    except KeyboardInterrupt:
        move.drive.off(brake=False)
        util.right.off(brake=False)
        util.left.off(brake=False)
        default = selected
        print("interrupted")
        #time.sleep(2)
    if stop:
        break

    