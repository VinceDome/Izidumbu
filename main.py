#a class for all functions that make the robot move using the motors and sensors
class Move:
    from ev3dev2.motor import *
    from ev3dev2.sensor import *
    from ev3dev2.sensor.lego import *
    from ev3dev2.sound import Sound
    from ev3dev2.led import Leds
    import os, time
    
    spkr = Sound()
    #Roberto
    drive = MoveTank(OUTPUT_B, OUTPUT_A)
    steer = MoveSteering(OUTPUT_B, OUTPUT_A)
    motorLeft = Motor(OUTPUT_B)
    motorRight = Motor(OUTPUT_A)

    gyro = GyroSensor(INPUT_2)
    colorSensorRight = ColorSensor(INPUT_1)
    colorSensorLeft = ColorSensor(INPUT_4)
    colorSensorMid = ColorSensor(INPUT_3)
    
    def boop(self):
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    #basic average calculator for two numbers
    def Avg(self, number1, number2):
        sum = number1 + number2
        return sum / 2 
     
    """
    #sappersrobot
    drive = MoveTank(OUTPUT_C, OUTPUT_B)
    steer = MoveSteering(OUTPUT_C, OUTPUT_B)
    motorb = Motor(OUTPUT_A) #baloldali motor
    motorLeft = Motor(OUTPUT_B) #jobb kerék
    motorRight = Motor(OUTPUT_C) #bal kerék
    motorc = Motor(OUTPUT_D) #jobo motor
    gyro = GyroSensor(INPUT_2)
    colorSensorRight = ColorSensor(INPUT_3)
    colorSensorLeft = ColorSensor(INPUT_4)
    """

    #moving forward with the gyro, while not resetting it at the start
    def g(self, speed, rot, initial_deg=False, multiplier=0.4, givenBrake=True, turnOffMotors = True, rampup=[0, 0], rampdown=[0, 0], timeout=10000):
        initial_rot = self.Avg(self.motorLeft.position, self.motorRight.position)
        
        if not initial_deg:
            initial_deg = self.gyro.angle
        
        diffU = (speed - rampup[0]) * -1
        diffD = (rampdown[0] - speed) * -1

        speed *= -1
        _speed = speed

        if speed < 0:
            multiplier *= -1
            rot *= -1

        tic = self.time.perf_counter()

        

        
        while True:
            #exits if the rot is passed
            if rot < 0 and initial_rot - self.Avg(self.motorLeft.position, self.motorRight.position) > rot * -1 or rot > 0 and self.Avg(self.motorLeft.position, self.motorRight.position) - initial_rot > rot:
                break
            elif self.time.perf_counter() > tic + timeout:
                break

            if not self.time.perf_counter() - tic > rampup[1]:
                ratio = (self.time.perf_counter() - tic) / rampup[1]
                speed = (ratio * diffU) - rampup[0]
            else:
                speed = _speed



            if rot < 0 and rampdown[1] != 0:
                if (rot * -1) - (initial_rot - self.Avg(self.motorLeft.position, self.motorRight.position)) < rampdown[1]:     
                    ratio = ((rot * -1) - (initial_rot - self.Avg(self.motorLeft.position, self.motorRight.position))) / rampdown[1]
                    speed = ((ratio * diffD) - rampdown[0])
            elif rot > 0 and rampdown[1] != 0:
                if rot - (self.Avg(self.motorLeft.position, self.motorRight.position) - initial_rot) < rampdown[1]:
                    ratio = rot - (self.Avg(self.motorLeft.position, self.motorRight.position) - initial_rot) / rampdown[1]
                    speed = (ratio * diffD) - rampdown[0]
            

            correction = (self.gyro.angle - initial_deg) * multiplier
            #print(correction, self.gyro.angle)

            if correction > 99:
                self.steer.on(100, speed)
                continue
            elif correction < -99:
                self.steer.on(-100, speed)
                continue

            
            print(speed)
            self.steer.on(correction, speed)

        if turnOffMotors:
            self.steer.off(brake=givenBrake)
       

        print(self.gyro.angle)
    
       #turns to a specified angle, but doesn't choose the shortest path
    def t(self, deg, tolerance, motors="ab", divider=4, timeout=10000):
        initial_deg = self.gyro.angle
        print(initial_deg)
        print(deg)
        


        tic = self.time.perf_counter()
        if initial_deg < deg:
            while self.gyro.angle < deg - tolerance:
                print("angle", self.gyro.angle)
                remaining = abs(deg - self.gyro.angle)
                print("remaining", remaining)
                
                if self.time.perf_counter() > tic + timeout:
                    break


                if remaining > 100:
                    if motors == "ab":
                        self.drive.on(-100, 100)
                    elif motors == "a":
                        self.drive.on(-100, 0)
                    elif motors == "b":
                        self.drive.on(0, 100)
                    continue
                elif remaining <= 3:
                   break
                elif remaining <= 10:
                    self.drive.on(-5, 5)
                    continue
                if motors == "ab":
                    print("driveleft:", remaining * -1 /divider, "driveright", {remaining/divider})
                    self.drive.on(remaining*-1/divider, remaining/divider)
                elif motors == "a":
                    self.drive.on(remaining*-1/2, 0)
                elif motors == "b":
                    self.drive.on(0, remaining/2)


        elif initial_deg > deg:
            while self.gyro.angle > deg + tolerance:
                remaining = abs(deg - self.gyro.angle)
                print("angle", self.gyro.angle)
                print("remaining", remaining)
                
                if self.time.perf_counter() > tic + timeout:
                    break

                if remaining > 100:
                    if motors == "ab":
                        self.drive.on(100, -100)
                    elif motors == "a":
                        self.drive.on(100, 0)
                    elif motors == "b":
                        self.drive.on(0, -100)
                    continue
                elif remaining <= 3:
                    break
                elif remaining <= 10:
                    self.drive.on(7, -7)
                    continue
                if motors == "ab":
                    print("driverigth:", remaining * -1 / divider, "driveleft", remaining/divider)
                    self.drive.on(remaining/divider, remaining*-1/divider)
                elif motors == "a":
                    self.drive.on(remaining/divider, 0)
                elif motors == "b":
                    self.drive.on(0, remaining*-1/divider)


        """
        elif 0 > deg:
            while (initial_deg + deg - self.gyro.angle)*-1 > 0:
                remaining = abs(initial_deg + deg) - abs(self.gyro.angle) * -1
                if initial_deg + deg:
                    print("geci")
                if remaining > 100:
                    self.drive.on(-100, 100)
                    continue
                if remaining < 30 and remaining > 20:
                    self.drive.on(-5, 5)
                    continue
                if remaining <= 20:
                    self.drive.on(-3, 3)
                    continue
                self.drive.on(remaining*-1/2, remaining/2)
        """




        self.drive.off()
        if self.time.perf_counter() > tic + timeout:
            return
        
        if tolerance == 0:
            print("ez már egy korrig")
            for i in range(4):
                print("újcheck")
                while deg < self.gyro.angle:
                    self.drive.on(1.5, -1.5)
                print("újcheck2")
                while deg > self.gyro.angle:
                    self.drive.on(-1.5, 1.5)
            self.drive.off()
            for i in range(5):
                print(self.gyro.angle)

    #turns a specified amount of degrees with the gyro
    def TurnWithDeg(self, deg):
        initial_deg = self.gyro.angle
        tolerance = 2

        print(deg)

        if 0 < deg:
            while initial_deg + deg - self.gyro.angle > 0:
                print("angle", self.gyro.angle)
                remaining = initial_deg + deg - self.gyro.angle
                print("remaining", remaining)
                if remaining > 100:
                    self.drive.on(100, -100)
                    continue
                elif remaining <= 3:
                    break
                elif remaining <= 10:
                    self.drive.on(7, -7)
                    continue
                print("driverigth:", remaining * -1 / 3.5, "driveleft", {remaining/3.5})
                self.drive.on(remaining/3, remaining*-1/3)
                


        if 0 > deg:
            print(initial_deg + deg - self.gyro.angle)
            while initial_deg + deg - self.gyro.angle < 0:
                remaining = abs(initial_deg + deg - self.gyro.angle)
                print("angle", self.gyro.angle)
                print("remaining", remaining)
                if remaining > 100:
                    self.drive.on(-100, 100)
                    continue
                elif remaining <= 3:
                   break
                elif remaining <= 10:
                    self.drive.on(-5, 5)
                    continue
                print("driveleft:", remaining * -1 / 3.5, "driveright", {remaining/3.5})
                self.drive.on(remaining*-1/3, remaining/3)


        """
        elif 0 > deg:
            while (initial_deg + deg - self.gyro.angle)*-1 > 0:
                remaining = abs(initial_deg + deg) - abs(self.gyro.angle) * -1
                if initial_deg + deg:
                    print("geci")
                if remaining > 100:
                    self.drive.on(-100, 100)
                    continue
                if remaining < 30 and remaining > 20:
                    self.drive.on(-5, 5)
                    continue
                if remaining <= 20:
                    self.drive.on(-3, 3)
                    continue
                self.drive.on(remaining*-1/2, remaining/2)
        """






        print("ez már egy korrig")
        self.drive.off()
        for i in range(4):
            print("újcheck")
            while initial_deg + deg < self.gyro.angle - tolerance:
                self.drive.on(-1.5, 1.5)
            print("újcheck2")
            while initial_deg + deg > self.gyro.angle + tolerance:
                self.drive.on(1.5, -1.5)
        self.drive.off()
        for i in range(5):
            print(self.gyro.angle)
    
    def ColorGyro(self, speed, initial_deg=False, multiplier=0.4, givenBrake=True, threshold = 5, mode="Black"):
        if not initial_deg:
            initial_deg = self.gyro.angle

        speed *= -1
        if speed < 0:
            multiplier *= -1

        while True:
            #exits if the rot is passed
            print("LIGTH", self.colorSensorRight.reflected_light_intensity)
            if mode == "Black":
                if self.colorSensorLeft.reflected_light_intensity < minLeft + threshold and self.colorSensorRight.reflected_light_intensity < minRight + threshold:
                    break
            elif mode == "White":
                if self.colorSensorLeft.reflected_light_intensity > maxLeft - threshold*2 and self.colorSensorRight.reflected_light_intensity > maxRight - threshold*2:
                    break
            correction = (self.gyro.angle - initial_deg) * multiplier
            print(correction, self.gyro.angle)
            if correction > 99:
                self.steer.on(-100, speed)
                continue
            elif correction < -99:
                self.steer.on(100, speed)
                continue
            self.steer.on(correction, speed)
        self.steer.off(brake=givenBrake)
        print(self.gyro.angle)
    
    
    #stops at a color, vErY uSeFuL
    def StopAtColor(self, speed, color="black", sensor="both"):
        speed *= -1
        self.drive.on(speed, speed)
        while True:
            if sensor == "both":
                if self.colorSensorLeft == color and self.colorSensorRight.color_name == color:
                    break
            elif sensor == "left":
                if self.colorSensorLeft.color_name == color:
                    break
            elif sensor == "right":
                if self.colorSensorRight.color_name == color:
                    break
        self.drive.off()

    
    #these two functions were only tests
    def FollowLine1(self, speed, color):
        initial_deg = self.gyro.angle
        correction = self.gyro.angle * 0.4 * -1
        if correction > 100:
            correction = 100
        if correction < -100:
            correction = -100
        while True:
            self.steer.on(0, speed)
            if self.gyro.angle > initial_deg + 3:
                while self.colorSensorLeft.color_name != color:
                    self.steer.on(correction, speed / 8)
            if self.gyro.angle < initial_deg - 3:
                while self.colorSensorLeft.color_name != color:
                    self.steer.on(correction, speed / 8)
        self.drive.off()
    def FollowLine2(self, speed, color):
        steeringValue = 20
        while True:
            self.steer.on(0, speed)
            if self.colorSensorLeft.color_name == "White":
                self.steer.on(steeringValue * -1, speed)
            if self.colorSensorLeft.color_name == "Black":
                self.steer.on(steeringValue, speed)

    #start of the pid line follower, WIP 
    def FollowLine(self, speed):
        global target
        Kp = 0.4
        Ki = 0.02-0.02
        Kd = 0
        error = 0
        integral = 0
        last_error = 0
        derivative = 0

        speed *= -1
        while True:
            error = (target - self.colorSensorRight.reflected_light_intensity)
            integral += error
            derivative = error - last_error

            toSteer = (error * Kp) + (integral * Ki) + (derivative * Kd)

            if toSteer > 100:
                toSteer = 100
            elif toSteer < -100:
                toSteer = -100

            self.steer.on(toSteer, speed)
            last_error = error
            print(toSteer) 
            
        
        
        
        """
        video on pid
        https://www.youtube.com/watch?v=AMBWV_HGYj4
        """

        
        #follow_line (in movetan) ---> a full working pid line follower already programmed
        
    #our own follower, still WIP
    def TrashLineFollower(self, speed, time):
        while True:
            left = self.colorSensorLeft.reflected_light_intensity
            right = self.colorSensorRight.reflected_light_intensity
            magicNumber = 0.5
            if left > right:
                correction = 2
            elif right > left:
                correction = 1
            else:
                correction = 0
            if correction == 1:
                self.steer.on(right * magicNumber, speed)
            elif correction == 2:
                self.steer.on(left * magicNumber, speed)
            else:
                self.steer.on(0, speed)

            #most kéne debugolni ebben a fázisban, de nem lehet, mert robotika pályánál vannak mások


    def Strafe(self, steer, speed, rot):
        initial_rot = self.Avg(self.motorLeft.position, self.motorRight.position)

        speed *= -1

        if 0 < speed:
            while self.Avg(self.motorLeft.position, self.motorRight.position) < initial_rot + rot:
                self.steer.on(steer, speed)
        elif speed < 0:
            while self.Avg(self.motorLeft.position, self.motorRight.position) > initial_rot - rot:
                self.steer.on(steer, speed)
        self.steer.off()   


#a class for all functions that use the motors for the attachments      
class Util:
    from ev3dev2.motor import *
    from ev3dev2.sensor import *
    from ev3dev2.sensor.lego import *
    from ev3dev2.led import Leds
    from ev3dev2.sound import Sound
    from ev3dev2.button import Button
    from ev3dev2.console import Console
    import os, time

    left = Motor(OUTPUT_C)
    right = Motor(OUTPUT_D)
    

#a class for storing the runs
class Runs:
    from ev3dev2.sound import Sound
    from main import Util, Move
    import time
    move = Move()
    util = Util()
    spkr = Sound()
    
    def pingpong(self):
        self.move.gyro.reset()
        for i in range(4):
            self.move.g(40, 1427, initial_deg=0)
            self.move.t(180, 1)
            self.move.g(40, 1427, initial_deg=180)
            self.move.t(0, 1) 

    def run1(self):
        self.move.gyro.reset()
        self.move.time.sleep(0.5)
        
        self.move.g(80, 2000, initial_deg=0, rampup=[0, 1], turnOffMotors = False)
        self.move.g(10, 400, rampup=[80, 1])
        

    def run2(self):
        self.move.gyro.reset()
        self.move.time.sleep(0.5)

        self.move.t(90, 1)
    def run3(self):
        pass
    def run4(self):
        pass
    def run5(self):
        pass

    

#a class for controlling the menu starting the runs
class Menu:
    from ev3dev2.motor import *
    from ev3dev2.sensor import *
    from ev3dev2.sensor.lego import *
    from ev3dev2.led import Leds
    from ev3dev2.sound import Sound
    from ev3dev2.button import Button
    from ev3dev2.console import Console
    move = Move()
    runs = Runs()
    util = Util()
    import os, time

    leds = Leds()
    #buttonS = TouchSensor()
    spkr = Sound()
    button = Button()
    console =  Console()

    #colors: BLACK, RED, GREEN, AMBER, ORANGE, YELLOW
    def speaking(self):
        self.sound.speak("Hoay mate!")

    def both(self, color):
        self.leds.set_color("LEFT", color)
        self.leds.set_color("RIGHT", color)



    def selection(self, default):

        self.both("GREEN")
        sleeptime = 0.3
        self.os.system("clear")
        number_of_runs = 5
        self.move.drive.off(brake=False)
        self.util.right.off(brake=False)
        self.util.left.off(brake=False)
        self.time.sleep(0.5)
        previous_selected = 0
        previous_gyro = 0
        selected = 0
        manualswitch = False
        motorcontrol = False
        motorWiggle = False
        currently_handling = -1
        gyroB = 0

        def printmenu():
            self.os.system("clear")
            printed_run = selected

            print("Run "+str(printed_run))
            print("Gyro "+str(self.move.gyro.angle))
            print(self.move.colorSensorMid.color_name)
       
        while True:
            diff = self.move.gyro.angle-gyroB
            if diff != 0:
                self.both("RED")
            else:
                self.both("GREEN")
            gyroB = self.move.gyro.angle

            if self.move.colorSensorMid.color_name in ["Black", "NoColor"]:
                selected = 0
                motorWiggle = True
                self.util.right.on(30)
                self.util.left.on(30)
                self.time.sleep(0.1)
                self.util.right.on(-30)
                self.util.left.on(-30)
                self.time.sleep(0.1)
            elif self.move.colorSensorMid.color_name == "Yellow":
                selected = 1

                if motorWiggle:
                    for i in range(3):
                        self.util.right.on(30)
                        self.util.left.on(30)
                        self.time.sleep(0.1)
                        self.util.right.on(-30)
                        self.util.left.on(-30)
                        self.time.sleep(0.1)
                    motorWiggle = False
                else:
                    self.util.left.on(10)
                    #self.util.right.on(3)
                    self.util.right.on(-20)
                    if self.util.left.is_stalled:
                        self.util.left.off()

            elif self.move.colorSensorMid.color_name == "White":
                selected = 2
                
                if motorWiggle:
                    for i in range(3):
                        self.util.right.on(30)
                        self.util.left.on(30)
                        self.time.sleep(0.1)
                        self.util.right.on(-30)
                        self.util.left.on(-30)
                        self.time.sleep(0.1)
                    motorWiggle = False
                else:
                    self.util.left.on(5)
                    self.util.right.on(10)
            elif self.move.colorSensorMid.color_name == "Red":
                selected = 3
                if motorWiggle:
                    for i in range(3):
                        self.util.right.on(30)
                        self.util.left.on(30)
                        self.time.sleep(0.1)
                        self.util.right.on(-30)
                        self.util.left.on(-30)
                        self.time.sleep(0.1)
                    motorWiggle = False
                else:
                    self.util.left.on(-5)
                    self.util.right.on(5)
            elif self.move.colorSensorMid.color_name == "Blue":
                selected = 5
                if motorWiggle:
                    for i in range(3):
                        self.util.right.on(30)
                        self.util.left.on(30)
                        self.time.sleep(0.1)
                        self.util.right.on(-30)
                        self.util.left.on(-30)
                        self.time.sleep(0.1)
                    motorWiggle = False
                else:
                    self.util.left.on(3)
                    self.util.right.on(-3)

            if self.button.enter and not self.button.down:
                self.util.right.off()
                self.util.left.off()
                self.both("ORANGE")
                self.os.system("clear")
                print("ARMED")
                
                while self.button.enter:
                    pass

                self.both("GREEN")

                if selected == 0:
                    print("FAILED")
                    printmenu()
                    continue

                return selected
            elif self.button.right or self.button.left:
                self.util.right.off(brake=False)
                self.util.left.off(brake=False)
                manualswitch = True
                break
            elif self.button.down:
                motorcontrol = True
                break
                         
            
                
            if selected != previous_selected or previous_gyro != self.move.gyro.angle:
                printmenu()
            previous_selected = selected
            previous_gyro = self.move.gyro.angle

        def printmenuM():
            self.os.system("clear")
            printed_run = selected

            print("Run "+str(printed_run))
            print("Gyro "+str(self.move.gyro.angle))
            print("MANUAL")

        if manualswitch:
            while True:
                diff = self.move.gyro.angle-gyroB
                if diff != 0:
                    self.both("RED")
                else:
                    self.both("GREEN")
                gyroB = self.move.gyro.angle

                try:
                    if self.button.right:

                        if selected == number_of_runs:
                            selected = 1
                            printmenuM()
                            self.time.sleep(sleeptime)
                            continue
                        
                        selected += 1
                        printmenuM()
                        self.time.sleep(sleeptime)

                    if self.button.left:
                        
                        if selected == 1 or selected == 0:
                            selected = number_of_runs
                            printmenuM()
                            self.time.sleep(sleeptime)

                            continue

                        selected -= 1
                        printmenuM()
                        self.time.sleep(sleeptime)
                        
                    if self.button.enter:
                        self.util.right.off()
                        self.util.left.off()
                        self.both("ORANGE")
                        self.os.system("clear")
                        print("ARMED")
                        
                        while self.button.enter:
                            pass

                        self.both("GREEN")
                        return selected

                    if previous_gyro != self.move.gyro.angle:
                        printmenuM()
                    previous_gyro = self.move.gyro.angle

                except KeyboardInterrupt:
                    return None
        elif motorcontrol:
            self.os.system("clear")
            print("motorCTRL")
            print("left")
            self.time.sleep(0.5)
            while True:
                if currently_handling == -1:
                    while self.button.left:
                        self.util.left.on(-20)
                    while self.button.right:
                        self.util.left.on(20)
                elif currently_handling == 1:  
                    while self.button.left:
                        self.util.right.on(-20)
                    while self.button.right:
                        self.util.right.on(20)
                

                if self.button.enter:
                    motorcontrol = False
                    return None
                elif self.button.down:
                    currently_handling *= -1
                    self.os.system("clear")
                    print("motorCTRL")
                    if currently_handling == -1: 
                        print("left")
                    elif currently_handling == 1: 
                        print("right")
                    self.time.sleep(0.2)

                self.util.right.off(brake=False)
                self.util.left.off(brake=False)

    def settarget(self, _target, _minLeft, _maxLeft, _minRight, _maxRight):
        global target, minLeft, maxLeft, minRight, maxRight
        target = _target
        minLeft = _minLeft
        maxLeft = _maxLeft
        minRight = _minRight
        maxRight = _maxRight

    def run(self, selected):
        
        
        if selected == 1:
            self.runs.run1()
            print("első futam done")
        elif selected == 2:
            self.runs.run2()
            print("második futam done")
        elif selected == 3:
            self.runs.run3()
            print("harmadik futam done")
        elif selected == 4:
            self.runs.run4()
            print("negyedik futam done")
        elif selected == 5:
            self.runs.run5()
            print("ötödik futam done")
            
        return None

        """
        exec("self.runs.run"+str(selected)+"()")
        print(str(selected)+" done.")     """
