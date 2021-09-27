#!/usr/bin/env micropython
from main import Menu, Move, Util
menu = Menu()
move = Move()
util = Util()
import time


stop = False
default = 1
menu.console.set_font("Lat15-Terminus32x16.psf.gz", True)
menu.time.sleep(2)
selected = 1
while True:
    try:
        while True:
            selected = menu.selection(default)
            default = menu.run(selected)
            #menu.time.sleep(1)
            if default == "end":
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