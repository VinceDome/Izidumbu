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
util.right.off(brake=False)
util.left.off(brake=False)