from main import Move, Util, Runs, Menu
import time
move = Move()
util = Util()
runs = Runs()
menu = Menu()


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



menu.settarget(30)
#-1734, -2682


move.gyro.reset()
time.sleep(0.5)



move.MoveWithGyro(-40, 250-70, initial_deg=0)
move.TurnToDeg(-50, 1)
move.MoveWithGyro(20, 500-50, initial_deg=-50)

move.MoveWithGyro(-40, 100, initial_deg=-50)
move.TurnToDeg(-30, 1)
util.left.on_for_degrees(40, 300)

move.TurnToDeg(-100, 1)
move.MoveWithGyro(40, 100, initial_deg=-100)
util.right.on_for_degrees(80, 300-80, brake=True)


move.MoveWithGyro(-25, 200, initial_deg=-100, givenBrake=False)
move.TurnToDeg(-80-10, 1)
move.MoveWithGyro(-40, 500, initial_deg=-80-10, givenBrake=False)

move.time.sleep(0.5)


move.MoveWithGyro(40, 300, initial_deg=-95)
util.right.on_for_degrees(-60, 350, block=False)
move.TurnToDeg(-165, 1)
move.MoveWithGyro(40, 200+200, initial_deg=-165)
move.TurnToDeg(-248, 1)


util.left.on_for_degrees(80, 900)


"""
util.right.on_for_seconds(5, 2)

move.time.sleep(1)

util.right.on_for_degrees(-40, 300)

move.time.sleep(0.5)

util.right.on_for_degrees(40, 500)
runs.spkr.beep(play_type=runs.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

#util.right.off()
move.time.sleep(0.5)

util.right.on_for_degrees(-40, 285)
runs.spkr.beep(play_type=runs.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

move.time.sleep(3)

"""

move.drive.off(brake=False)
util.right.off(brake=False)
util.left.off(brake=False)



