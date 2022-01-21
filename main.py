#a class for all functions that make the robot move using the motors and sensors
class Move:
    from ev3dev2.motor import *
    from ev3dev2.sensor import *
    from ev3dev2.sensor.lego import *
    from ev3dev2.led import Leds
    import os, time
    
    
    #Roberto
    drive = MoveTank(OUTPUT_B, OUTPUT_A)
    steer = MoveSteering(OUTPUT_B, OUTPUT_A)
    motorLeft = Motor(OUTPUT_B)
    motorRight = Motor(OUTPUT_A)

    gyro = GyroSensor(INPUT_2)
    colorSensorRight = ColorSensor(INPUT_1)
    colorSensorLeft = ColorSensor(INPUT_4)
    colorSensorMid = ColorSensor(INPUT_3)
    
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
    def MoveWithGyro(self, speed, rot, initial_deg=False, multiplier=0.4, givenBrake=True):
        initial_rot = self.Avg(self.motorLeft.position, self.motorRight.position)
        if not initial_deg:
            initial_deg = self.gyro.angle

        speed *= -1

        if speed < 0:
            multiplier *= -1
            rot *= -1
        while True:
            #exits if the rot is passed
            if rot < 0 and initial_rot - self.Avg(self.motorLeft.position, self.motorRight.position) > rot * -1 or rot > 0 and self.Avg(self.motorLeft.position, self.motorRight.position) > initial_rot + rot:
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
    
    def ColorGyro(self, speed, initial_deg=False, multiplier=0.4, givenBrake=True):
        if not initial_deg:
            initial_deg = self.gyro.angle

        speed *= -1

        if speed < 0:
            multiplier *= -1

        while True:
            #exits if the rot is passed
            print("LIGTH", self.colorSensorRight.reflected_light_intensity)
            if self.colorSensorRight.reflected_light_intensity < 15:
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

    #turns to a specified angle, but doesn't choose the shortest path
    def TurnToDeg(self, deg, tolerance, motors="ab", divider=4):
        initial_deg = self.gyro.angle
        print(initial_deg)
        print(deg)
        



        if initial_deg < deg:
            while self.gyro.angle < deg - tolerance:
                print("angle", self.gyro.angle)
                remaining = abs(deg - self.gyro.angle)
                print("remaining", remaining)
                
                if remaining > 100:
                    self.drive.on(-100, 100)
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


        if initial_deg > deg:
            while self.gyro.angle > deg + tolerance:
                remaining = abs(deg - self.gyro.angle)
                print("angle", self.gyro.angle)
                print("remaining", remaining)
                
                
                if remaining > 100 and divider >= 3:
                    self.drive.on(100, -100)
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

    #basic average calculator for two numbers
    def Avg(self, number1, number2):
        sum = number1 + number2
        return sum / 2 
     
    #stops at a color, vErY uSeFuL
    def StopAtColor(self, color, speed):
        speed *= -1
        self.drive.on(speed, speed)
        while True:
            if self.colorSensorLeft.color_name == color:
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
    
    def updown(self):
        self.left.on(100)
        self.time.sleep(1.5)
        self.left.off()
        self.left.on_for_seconds(-100, 4)

    def up(self):
        self.left.on_for_seconds(100, 1)

    def down(self):
        self.left.on_for_seconds(-100, 1, block=False)

    def five(self):
        self.right.on_for_seconds(-50, 0.2)
        self.time.sleep(0.5)
        self.right.on_for_seconds(50, 1, brake=False, block=False)


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
            self.move.MoveWithGyro(40, 1427)
            self.move.TurnToDeg(180, 1)
            self.move.MoveWithGyro(40, 1427)
            self.move.TurnToDeg(0, 1)   

    
    def run2(self):
        self.move.gyro.reset()
        self.time.sleep(0.5)
        self.util.right.on(-10)
        self.move.time.sleep(0.5)
        self.util.right.off(brake=True)

        self.move.MoveWithGyro(40, 800+40, givenBrake=False, initial_deg=3-1-1, multiplier = 0.8)
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        self.util.right.on_for_degrees(40, 80+80, brake=True, block=False)

        #self.move.MoveWithGyro(40, 40, initial_deg=2+3-1)
        """
        self.move.MoveWithGyro(40, 100, initial_deg=-50, givenBrake=False)
        self.move.MoveWithGyro(40, 1000-500-200, initial_deg=45, givenBrake=False)
        
        self.move.MoveWithGyro(40, 500+200, initial_deg=30, givenBrake=False)
        self.move.MoveWithGyro(20, 150+150-150, initial_deg=30, givenBrake=False)
        """
        
        self.move.MoveWithGyro(40, 700+400, initial_deg=30, givenBrake=False, multiplier=0.6)
        self.move.MoveWithGyro(20, 150, initial_deg=30, givenBrake=False)

        self.move.gyro.reset()
        self.time.sleep(0.5)
        self.move.MoveWithGyro(-40, 250-70, initial_deg=0)
        self.move.TurnToDeg(-50, 1)
        self.move.MoveWithGyro(20, 500-50, initial_deg=-50)
        
        #teteje -169
        #első kienged -12
        #második kienged 600??? xddd
        #első kidobás

        
        self.move.MoveWithGyro(-40, 100, initial_deg=-50)
        self.move.TurnToDeg(-30, 1)
        self.util.left.on_for_degrees(40, 300)
        

        self.move.TurnToDeg(-100, 1)
        self.move.MoveWithGyro(40, 100, initial_deg=-100)
        self.util.right.on_for_degrees(80, 300-80, brake=True)


        self.move.MoveWithGyro(-25, 200, initial_deg=-100, givenBrake=False)
        self.move.TurnToDeg(-80-10, 1)
        self.move.MoveWithGyro(-40, 500, initial_deg=-80-10, givenBrake=False)
        """
        self.move.MoveWithGyro(-40, 150, initial_deg=-100, givenBrake=False)
        self.move.MoveWithGyro(-40, 50, initial_deg=-60, givenBrake=False)
        self.move.MoveWithGyro(-40, 430, initial_deg=-80, givenBrake=False)
        """

        self.move.time.sleep(0.5)


        self.move.MoveWithGyro(40, 300, initial_deg=-95)
        self.util.right.on_for_degrees(-60, 350, block=False)
        self.move.TurnToDeg(-165, 1)
        self.move.MoveWithGyro(40, 200+200, initial_deg=-165)
        self.move.TurnToDeg(-248, 1)
        """
        self.move.MoveWithGyro(40, 100, initial_deg=-120, givenBrake=False)
        self.move.MoveWithGyro(40, 300, initial_deg=-180, givenBrake=False)
        self.move.ColorGyro(40, initial_deg=-180)
        self.move.TurnToDeg(-220, 1)
        """

        """
        self.move.MoveWithGyro(40, 50, initial_deg=-150, givenBrake=False)
        self.move.MoveWithGyro(40, 450-50, initial_deg=-220, givenBrake=False)
        self.move.TurnToDeg(-280, 1)
        """
        self.util.left.on_for_degrees(80, 900)
        
    def run3(self):
        self.move.gyro.reset()
        self.time.sleep(0.5)
        
        self.util.left.on_for_seconds(3, 2)
        self.util.right.on_for_seconds(5, 2, block=False)
        
        self.move.MoveWithGyro(-40, 1100-200, initial_deg=5, multiplier = 0.5)
        self.move.MoveWithGyro(-40, 200+100-100, initial_deg=0, multiplier = 0.6)

        self.move.steer.on_for_degrees(0, 40, 150)

        #lecsap mindent
        self.util.left.on_for_degrees(-40, 300+100, block=False)
        self.util.right.on_for_degrees(-40, 300)
        
        
        self.move.time.sleep(0.5)
        
        #felemeli a repülőgép oldali kart
        self.util.right.on_for_degrees(40, 500)
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        self.util.right.on_for_degrees(-40, 275)
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

        #kicsit előre megy, felemeli a motort
        self.move.MoveWithGyro(20, 60, initial_deg=0)
        self.util.left.on_for_degrees(20, 300)

        #hazajön
        self.move.MoveWithGyro(40, 300, initial_deg=30, multiplier = 0.7)
        self.util.right.on_for_degrees(-40, 100)
        self.move.MoveWithGyro(80, 700, initial_deg=90, multiplier = 0.6)



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
    sound = Sound()
    button = Button()
    console =  Console()

    #colors: BLACK, RED, GREEN, AMBER, ORANGE, YELLOW
    def speaking(self):
        self.sound.speak("Hoay mate!")

    def both(self, color):
        self.leds.set_color("LEFT", color)
        self.leds.set_color("RIGHT", color)

    def selection(self, default):
        sleeptime = 0.3
        self.os.system("clear")
        number_of_runs = 4
        self.move.drive.off(brake=False)
        self.util.right.off(brake=False)
        self.util.left.off(brake=False)
        self.time.sleep(0.5)
        previous_selected = 0
        previous_gyro = 0
        selected = 0
        manualswitch = False
        motorhandling = False
        currently_handling = -1
        self.os.system("clear")
        print("Run "+str(selected))
        print("Gyro "+str(self.move.gyro.angle))
        print(self.move.colorSensorMid.color_name)
        while True:
            
            if self.move.colorSensorMid.color_name in ["Black", "NoColor"]:
                selected = 0
            
            elif self.move.colorSensorMid.color_name == "Brown":
                selected = 1
            elif self.move.colorSensorMid.color_name == "Red":
                selected = 2
            elif self.move.colorSensorMid.color_name == "White":
                selected = 3
            elif self.move.colorSensorMid.color_name == "Blue":
                selected = 4


            if self.button.enter and not self.button.down:
                self.os.system("clear")
                print("STARTING")
                if selected == 0:
                    print("FAILED")
                    self.os.system("clear")
                    print("Run "+str(selected))
                    print("Gyro "+str(self.move.gyro.angle))
                    print(self.move.colorSensorMid.color_name)
                    continue
                return selected
            elif self.button.right or self.button.left:
                manualswitch = True
                break
            elif self.button.down:
                if self.button.enter:
                    self.util.right.off(brake=False)
                    self.util.left.off(brake=False)
                    motorhandling = True
                    break

                self.util.right.on(30)
                self.util.left.on(30)
                self.time.sleep(0.1)
                self.util.right.on(-30)
                self.util.left.on(-30)
                self.time.sleep(0.1)
            else:
                self.util.right.off(brake=False)
                self.util.left.off(brake=False)
            
            if selected != previous_selected or previous_gyro != self.move.gyro.angle:
                self.os.system("clear")
                print("Run "+str(selected))
                print("Gyro "+str(self.move.gyro.angle))
                print(self.move.colorSensorMid.color_name)
            previous_selected = selected
            previous_gyro = self.move.gyro.angle

        if manualswitch:
            while True:
                try:
                    if self.button.right:

                        if selected == number_of_runs:
                            selected = 1
                            self.os.system("clear")
                            print("Run "+str(selected))
                            print("Gyro "+str(self.move.gyro.angle))
                            print("MANUAL")
                            self.time.sleep(sleeptime)
                            continue
                        
                        self.os.system("clear")
                        selected += 1
                        print("Run "+str(selected))
                        print("Gyro "+str(self.move.gyro.angle))
                        print("MANUAL")
                        self.time.sleep(sleeptime)

                    if self.button.left:
                        
                        if selected == 1:
                            selected = number_of_runs
                            self.os.system("clear")
                            print("Run "+str(selected))
                            print("Gyro "+str(self.move.gyro.angle))
                            print("MANUAL")
                            self.time.sleep(sleeptime)

                            continue

                        selected -= 1
                        self.os.system("clear")
                        print("Run "+str(selected))
                        print("Gyro "+str(self.move.gyro.angle))
                        print("MANUAL")
                        self.time.sleep(sleeptime)
                        
                    if self.button.enter:
                        self.time.sleep(0.5)
                        return selected

                    if previous_gyro != self.move.gyro.angle:
                        self.os.system("clear")
                        print("Run "+str(selected))
                        print("Gyro "+str(self.move.gyro.angle))
                        print("MANUAL")
                    previous_gyro = self.move.gyro.angle

                except KeyboardInterrupt:
                    return None
        elif motorhandling:
            self.os.system("clear")
            print("motorhandling")
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
                    motorhandling = False
                    return None
                elif self.button.down:
                    currently_handling *= -1
                    self.os.system("clear")
                    print("motorhandling")
                    if currently_handling == -1: 
                        print("left")
                    elif currently_handling == 1: 
                        print("right")
                    self.time.sleep(0.2)

                self.util.right.off(brake=False)
                self.util.left.off(brake=False)

    def settarget(self, _target):
        global target
        target = _target

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
        if selected == 4:
            self.runs.run4()
            print("negyedik futam done")
            return "end"
        return None

        """
        exec("self.runs.run"+str(selected)+"()")
        print(str(selected)+" done.")     """








