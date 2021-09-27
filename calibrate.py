#!/usr/bin/env micropython
from main import Menu, Move
move = Move()
menu = Menu()
move.gyro.calibrate()
move.time.sleep(1)
menu.console.set_font("Lat15-Terminus32x16.psf.gz", True)
print("kalibráltam")
move.MoveWithGyro(100, 10, initial_deg = 0)
move.MoveWithGyro(-100, 10, initial_deg = 0)