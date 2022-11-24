#!/usr/bin/env micropython
from main import Menu, Move, Runs, Util
import time
move = Move()
menu = Menu()
util = Util()
runs = Runs()

menu.console.set_font("Lat15-Terminus32x16.psf.gz", True)
menu.both("GREEN")
move.drive.off(brake=False)
util.lever.off(brake=False)
util.topping.off(brake=False)