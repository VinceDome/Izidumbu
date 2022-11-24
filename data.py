from main import  Move, Util
import os
move = Move()
util = Util()

while True:
    print("Gyro:", move.gyro.angle)
    print("Leftwheel", move.motorLeft.position)
    print("Rightwheel", move.motorRight.position)

    print("Topping motor", util.topping.position)
    print("Lever", util.lever.position)
    os.system("clear")
 





