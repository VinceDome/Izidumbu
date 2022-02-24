#!/usr/bin/env micropython
from main import Menu, Move, Runs, Util
import time
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

move.gyro.reset()
time.sleep(0.5)

move.motorLeft.on_for_seconds(-40, 3.5)
move.steer.off()

move.drive.off(brake=False)
util.right.off(brake=False)
util.left.off(brake=False)



