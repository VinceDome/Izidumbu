#!/usr/bin/env micropython
from main import Menu, Move, Runs, Util
import time, random
move = Move()
menu = Menu()
util = Util()
runs = Runs()
menu.console.set_font("Lat15-Terminus32x16.psf.gz", True)


def calibrate():
    move.gyro.calibrate()
    print("kalibráltam")

def troll(direction="backward"):
    if direction == "forward":
        move.MoveWithGyro(1, 500)
    else:
        move.MoveWithGyro(-1, 500)

def gyroprint():
    while True:
        print(move.gyro.angle)

def ganyolo():
    move.motorLeft.on(30)
    for i in range(30, -1, -1):
        move.os.system("clear")
        print(i)
        move.time.sleep(1)
    move.motorLeft.off()
    move.motorRight.on(30)
    for i in range(30, -1, -1):
        move.os.system("clear")
        print(i)
        move.time.sleep(1)

def speed():
    for i in range(1, 100):
        move.MoveWithGyro(i, 50, initial_deg=0, givenBrake=False)



menu.settarget(30, 0, 0, 0, 0)
#-1734, -2682



runs.run1()

move.time.sleep(5)
"""
move.gyro.reset()
move.time.sleep(0.5)
"""




"""
for i in range(30):
    fok = random.randint(-300, 300)
    move.t(fok)
    time.sleep(0.5)
    print(fok, move.gyro.angle)

"""
"""
gyroB = 0
gyroBL = [0]


menu.both("GREEN")
while True:
    diff = move.gyro.angle-gyroB
    print(diff)
    

    if not min(gyroBL) < max(gyroBL) - 10:
        if max(gyroBL) > 5 or min(gyroBL) < -5:
            if len(gyroBL) <= 38:
                break
    
    gyroBL.append(diff)
    if len(gyroBL) >= 40:
        del gyroBL[0]
    gyroB = move.gyro.angle
    time.sleep(0.05)

menu.both("RED")
time.sleep(2)

"""
move.drive.off(brake=False)
util.lever.off(brake=False)
util.topping.off(brake=False)

 





