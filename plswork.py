from main import Move, Util, Runs, Menu
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

"""
util.left.on_for_degrees(40, 300)
move.time.sleep(2)
util.left.on_for_degrees(80, 900)
"""

move.TurnWithDeg(180)
#runs.run3()


move.drive.off(brake=False)
util.right.off(brake=False)
util.left.off(brake=False)



