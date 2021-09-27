#!/usr/bin/env micropython
from main import Menu, Move
move = Move()
menu = Menu()
menu.console.set_font("Lat15-Terminus32x16.psf.gz", True)


def ganyolo():
    move.motora.on(30)
    for i in range(30, -1, -1):
        move.os.system("clear")
        print(i)
        move.time.sleep(1)
    move.motora.off()
    move.motord.on(30)
    for i in range(30, -1, -1):
        move.os.system("clear")
        print(i)
        move.time.sleep(1)

ganyolo()