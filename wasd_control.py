from main import Menu, Move, Util
menu = Menu()
move = Move()
util = Util()
import time, os, keyboard
speed = 80

while True:
    _move = 0
    steer = 0

    if keyboard.is_pressed("escape"):
        break
    if keyboard.is_pressed("w"):
        _move += speed
    if keyboard.is_pressed("s"):
        _move -= speed
    if keyboard.is_pressed("a"):
        steer -= speed/2
    if keyboard.is_pressed("d"):
        steer += speed/2
    if 0 <= _move:
        driveLeft = _move + steer
        driveRight = _move + (-1*steer)
    else:
        driveLeft = _move + (-1*steer)
        driveRight = _move + steer

    move.drive(driveLeft, driveRight)
    os.system("cls")


