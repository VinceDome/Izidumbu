#!/usr/bin/env micropython
from main import Menu, Move
move = Move()
menu = Menu()

menu.both("RED")
move.gyro.calibrate()
menu.both("GREEN")
move.time.sleep(0.5)
menu.console.set_font("Lat15-Terminus32x16.psf.gz", True)
print("kalibráltam")
move.g(100, 10, initial_deg = 0)
move.g(-100, 10, initial_deg = 0, givenBrake=False)