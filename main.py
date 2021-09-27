#a class for all functions that make the robot move using the motors and sensors
class Move:
    from ev3dev2.motor import *
    from ev3dev2.sensor import *
    from ev3dev2.sensor.lego import *
    from ev3dev2.led import Leds
    import os, time
    
    """
    #Roberto
    drive = MoveTank(OUTPUT_A, OUTPUT_D)
    steer = MoveSteering(OUTPUT_A, OUTPUT_D)
    motora = Motor(OUTPUT_A)
    motord = Motor(OUTPUT_D)
    gyro = GyroSensor(INPUT_1)
    colorSensorRight = ColorSensor(INPUT_3)
    colorSensorLeft = ColorSensor(INPUT_4)
    """
    #sappersrobot
    drive = MoveTank(OUTPUT_C, OUTPUT_B)
    steer = MoveSteering(OUTPUT_C, OUTPUT_B)
    motorb = Motor(OUTPUT_A) #baloldali motor
    motora = Motor(OUTPUT_B) #jobb kerék
    motord = Motor(OUTPUT_C) #bal kerék
    motorc = Motor(OUTPUT_D) #jobo motor
    gyro = GyroSensor(INPUT_2)
    colorSensorRight = ColorSensor(INPUT_3)
    colorSensorLeft = ColorSensor(INPUT_4)


    #moving forward with the gyro, while not resetting it at the start
    def MoveWithGyro(self, speed, rot, initial_deg=False, multiplier=0.4, givenBrake=True):
        initial_rot = self.Avg(self.motora.position, self.motord.position)
        if not initial_deg:
            initial_deg = self.gyro.angle
    
        if speed < 0:
            multiplier *= -1
            rot *= -1
        while True:
            #exits if the rot is passed
            if rot < 0 and initial_rot - self.Avg(self.motora.position, self.motord.position) > rot * -1 or rot > 0 and self.Avg(self.motora.position, self.motord.position) > initial_rot + rot:
                break
            correction = (self.gyro.angle - initial_deg) * multiplier * -1
            print(correction)
            if correction > 99:
                self.steer.on(100, speed)
                continue
            elif correction < -99:
                self.steer.on(-100, speed)
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
    def TurnToDeg(self, deg, tolerance, motors="ad", divider=3):
        initial_deg = self.gyro.angle
        print(initial_deg)
        print(deg)
        



        if initial_deg < deg:
            while self.gyro.angle < deg - tolerance:
                print("angle", self.gyro.angle)
                remaining = abs(deg - self.gyro.angle)
                print("remaining", remaining)
                if remaining > 100 and divider >= 3:
                    self.drive.on(100, -100)
                    continue
                elif remaining <= 3:
                    break
                elif remaining <= 10:
                    self.drive.on(7, -7)
                    continue
                if motors == "ad":
                    print("driverigth:", remaining * -1 / divider, "driveleft", remaining/divider)
                    self.drive.on(remaining/divider, remaining*-1/divider)
                elif motors == "a":
                    self.drive.on(remaining/2, 0)
                elif motors == "d":
                    self.drive.on(0, remaining*-1/2)
                


        if initial_deg > deg:
            while self.gyro.angle > deg + tolerance:
                remaining = abs(deg - self.gyro.angle)
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
                if motors == "ad":
                    print("driveleft:", remaining * -1 /divider, "driveright", {remaining/divider})
                    self.drive.on(remaining*-1/divider, remaining/divider)
                elif motors == "a":
                    self.drive.on(remaining*-1/2, 0)
                elif motors == "d":
                    self.drive.on(0, remaining/2)


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
                    self.drive.on(-1.5, 1.5)
                print("újcheck2")
                while deg > self.gyro.angle:
                    self.drive.on(1.5, -1.5)
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
        target = 27.5
        Kp = 1.5
        Ki = 0.02
        Kd = 7
        error = 0
        integral = 0
        last_error = 0
        derivative = 0
        while True:
            error = (target - self.colorSensorLeft.reflected_light_intensity)
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
        initial_rot = self.Avg(self.motora.position, self.motord.position)
        if 0 < speed:
            while self.Avg(self.motora.position, self.motord.position) < initial_rot + rot:
                self.steer.on(steer, speed)
        elif speed < 0:
            while self.Avg(self.motora.position, self.motord.position) > initial_rot - rot:
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

    left = Motor(OUTPUT_B)
    right = Motor(OUTPUT_C)
    
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
    from main import Util, Move
    import time
    move = Move()
    util = Util()

    #kosár és a másik térfélre áttóni
    def run1(self):
        #values = open("values.txt", "a+")
        #values.write("\n------------------------------------\nGYRO AZ ELEJÉN: " + str(self.move.gyro.angle))
        self.move.gyro.reset()
        #values.write("\nSLEEP ELŐTT: " + str(self.move.gyro.angle))
        self.move.time.sleep(0.5)
        #values.write("\nSLEEP UTÁN: " + str(self.move.gyro.angle))
        #values.close()
        self.util.left.on_for_seconds(-100, 1, block=False)

        
        self.move.MoveWithGyro(55+20, 1290, initial_deg=0)
    
        #befordul, rámegy, felemeli-leengedi, visszamegy
        self.move.TurnToDeg(-77-2-2, 1)
        self.move.MoveWithGyro(40, 500, initial_deg=-79-2)
        self.util.left.on_for_degrees(100, 950+950+300)
        self.time.sleep(0.5)
        self.util.left.on_for_degrees(-100, 950+950+300, block=False) #1007 - 782 = 225
        self.time.sleep(0.3)
        self.move.MoveWithGyro(-40, 267)
        

        #leszedi a kockát
        self.move.TurnToDeg(-211+2, 1)

        """
        self.move.time.sleep(0.2)
        self.move.TurnToDeg(-211+2, 0)
        """
        self.move.MoveWithGyro(-50, 240, initial_deg=-211+2)
        self.move.MoveWithGyro(-20, 120, initial_deg=-211+2)
        self.move.MoveWithGyro(60, 500, initial_deg=-211+2)

        """
        #felkapja a health unitot
        self.move.TurnToDeg(-349, 0)
        self.util.left.on(-50, block=False)
        self.util.left.on_for_degrees(50, 260+60+90, block=False)
        self.move.MoveWithGyro(40, 390-60, givenBrake=True)
        self.move.TurnToDeg(-352, 0)
        self.move.MoveWithGyro(40, 60, givenBrake=False)
        
        self.move.time.sleep(0.5)
        self.util.left.on_for_seconds(50, 2)
        self.move.time.sleep(0.5)
        
        #visszamegy
        self.move.MoveWithGyro(-40, 370, givenBrake=False)


        #ráfurdul a hazaútra, kimegy és kisodorja a health unitot
        self.move.TurnToDeg(-453, 0, divider = 5) #-104+3
        """
        #ráfordul a hazaútra, kimegy és kisodorja a health unitot
        self.move.TurnToDeg(-98, 1)
        self.move.MoveWithGyro(80, 800, initial_deg = -98)
        self.move.Strafe(-25, 90, 800)

        

    #háttal betolja a lépésszámlálót, megfordul, kerékkel meghajtja a futópadot vagy mit, elhúzza a kereket és hazaviszi a másikat
    def run2(self):

        
        self.util.right.on_for_seconds(100, 2)
        self.move.gyro.reset()
        self.move.time.sleep(0.5)
        #self.move.MoveWithGyro(-50, 1400-800, 5)
        #self.move.MoveWithGyro(-50, 1100+250, 10)
        self.move.MoveWithGyro(-50, 1950-200, 5)
        




        #falaz a step counter után
        self.move.MoveWithGyro(30, 100)
        self.move.TurnToDeg(80, 2, "a")
        self.move.MoveWithGyro(-20, 200)
        self.move.time.sleep(0.3)
        self.move.gyro.reset()
        self.move.time.sleep(0.4)

        #odamegy a futópadhoz
        self.move.MoveWithGyro(30, 40)
        self.move.TurnToDeg(15, 1)
        self.move.MoveWithGyro(40, 200)

        """
        #nagyobb ív
        self.move.TurnToDeg(70, 1)
        self.move.MoveWithGyro(60, 350, initial_deg=70, givenBrake=False)
        self.move.MoveWithGyro(60, 450, initial_deg=110)
        self.move.TurnToDeg(115, 1)
        self.move.MoveWithGyro(30, 400+50+200, initial_deg=115)
        """
        
        #eredeti ív
        self.move.TurnToDeg(70, 1)
        self.move.MoveWithGyro(60, 650+150, initial_deg=105)
        self.move.TurnToDeg(115, 1)
        self.move.MoveWithGyro(30, 400+50, initial_deg=115)
        

        #meghajtja a futópadot
        self.move.TurnToDeg(90, 1)
        self.move.MoveWithGyro(30, 500, initial_deg=90)
        #self.move.MoveWithGyro(-20, 10)
        self.util.left.on_for_seconds(100, 2)
        
        


    
        #futópad után falaz
        self.util.right.on(100)
        self.move.TurnToDeg(90, 0)
        self.move.MoveWithGyro(-40, 35, initial_deg=90)
        self.move.TurnToDeg(0, 0)
        self.move.MoveWithGyro(-20, 200, initial_deg=0)
        self.time.sleep(0.3)
        self.move.gyro.reset()
        self.time.sleep(0.2)

        #rámegy a kekw kerékre
        self.move.MoveWithGyro(50, 680, initial_deg=0)
        self.move.TurnToDeg(67, 1)
        self.move.MoveWithGyro(20, 6, givenBrake=False, initial_deg=67)

        #megfogja a kekw kereket
        self.util.right.on_for_degrees(-50, 228+50)
        self.time.sleep(0.4)
        
        #kihúzza a kék kereket
        self.move.MoveWithGyro(-30*0.5, 150, initial_deg=67)
        self.move.TurnToDeg(40, 1, "a")
        self.time.sleep(0.3)
        self.util.right.on(50)
        self.time.sleep(0.3)

        #rámegy a nagy kerékre
        self.move.MoveWithGyro(-40, 170, initial_deg=40)
        self.move.TurnToDeg(-57, 1, "a")
        self.move.MoveWithGyro(40, 140, initial_deg=-57, givenBrake=False)
        
        
        
        #ráfog a nagy kerékre
        self.util.right.on_for_degrees(-40, 160-30+7)
        self.move.time.sleep(0.5)

        #hazajön
        self.move.MoveWithGyro(-40, 50)
    
        self.move.TurnToDeg(-105, 1)
        self.move.MoveWithGyro(90, 2700, -110, givenBrake=False, multiplier=0.7)

        #self.move.MoveWithGyro(70, 2000, -150, givenBrake=False)
        self.util.right.on_for_seconds(50, 1)
        

        

    #padba kockák és innovation project
    def run3(self):
        self.move.gyro.reset()
        self.move.time.sleep(0.5)
        self.move.MoveWithGyro(60, 60, givenBrake=False, initial_deg=0) 
        self.move.time.sleep(0.1)

    
        self.move.TurnToDeg(-29, 0+1)
        #self.move.TurnToDeg(-29, 0)
        
        self.move.MoveWithGyro(40, 345+10, initial_deg=-29)

        self.move.TurnToDeg(13-1, 0+1)
        #self.move.TurnToDeg(13-1, 0)

        self.time.sleep(0.3)
        
        
        self.move.MoveWithGyro(60, 250, initial_deg=12, givenBrake=False)
        self.move.MoveWithGyro(30, 150, initial_deg=12)
        self.move.Strafe(30, 40, 300+400)
        
        self.move.time.sleep(0.5)
        self.move.MoveWithGyro(-40, 600)

        #self.move.MoveWithGyro(-70, 700)
        #self.move.TurnToDeg(-5, 1)
        #self.move.MoveWithGyro(-50, 500)
        

    #a csúszdáról hazaviszi az embert
    def run4(self):
        self.move.gyro.reset()
        self.move.time.sleep(0.5)
        
        #új rész
        self.util.right.on(50)
    
        #self.move.MoveWithGyro(80, 950, initial_deg=-2, givenBrake=False, multiplier=0.6)
        self.move.MoveWithGyro(80, 900, initial_deg=0, givenBrake=False, multiplier=0.6)
        self.move.MoveWithGyro(10, 50, initial_deg=0, givenBrake=False)
        self.move.TurnToDeg(0, -2)
        
        self.move.time.sleep(0.5)
        self.util.right.on(-50)
        self.move.time.sleep(1.5)
        
        self.move.MoveWithGyro(-30, 200, givenBrake=False, initial_deg=0)
        self.move.MoveWithGyro(-50, 500-200, givenBrake=False, initial_deg=0)
        self.move.MoveWithGyro(-80, 1700*1.5, initial_deg=40)
        
        """
        #régi rész
        self.util.right.on(-40, block=True)
        self.move.time.sleep(0.4)
        self.move.MoveWithGyro(80, 800, givenBrake=False)
        self.util.right.on(40)
        self.util.time.sleep(0.3)
        self.util.right.off(brake=False)
        self.util.time.sleep(0.5)

        self.move.Strafe(-5, -80, 1200)
        """

    #crosses gate, drops cubes and dances like there's no tomorrow
    def run5(self):
        self.move.gyro.reset()
        self.move.time.sleep(0.5)
        #turns to the right degree
        self.util.right.on_for_seconds(50, 1)
        self.move.MoveWithGyro(80, 1400, initial_deg=0)
        self.move.TurnToDeg(-30, 1)
        self.move.MoveWithGyro(80, 410-30, initial_deg=-30)
        self.move.TurnToDeg(-90, 1)

        #goes through the gate and drops the cubes
        self.move.MoveWithGyro(80, 920, givenBrake=False, initial_deg=-90)
        self.time.sleep(1)
        self.util.five()
        self.time.sleep(0.5)

        #goes to the dance floor
        self.move.MoveWithGyro(-40, 300)
        self.move.TurnToDeg(-140, 1)
        self.move.MoveWithGyro(80, 750, initial_deg=-140)

        #drops them sick moves
        self.move.TurnToDeg(-370, 50)
        while True:
            self.move.TurnToDeg(-25, 50)
            self.move.TurnToDeg(60, 50)
            self.move.TurnToDeg(200, 50)
            self.move.TurnToDeg(-380, 50)

    def pingpong(self):
        self.move.gyro.reset()
        for i in range(4):
            self.move.MoveWithGyro(40, 1427)
            self.move.TurnToDeg(180, 1)
            self.move.MoveWithGyro(40, 1427)
            self.move.TurnToDeg(0, 1)


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
        selected = default
        self.os.system("clear")
        number_of_runs = 5
        self.move.drive.off(brake=False)
        self.util.right.off(brake=False)
        self.util.left.off(brake=False)
        if selected > number_of_runs:
            print("Leálljon a program?")
            while True:
                if self.button.enter:
                    return "end"
                elif self.button.left:
                    selected = number_of_runs
                    self.time.sleep(sleeptime)
                    break
        self.os.system("clear")
        print(selected)
        self.time.sleep(0.5)
        while True:
            if self.button.right:
                if selected == number_of_runs:
                    self.os.system("clear")
                    selected = 1
                    print(selected)
                    self.time.sleep(sleeptime)
                    continue
                self.os.system("clear")
                selected += 1
                print(selected)
                self.time.sleep(sleeptime)
            if self.button.left:
                if selected == 1:
                    self.os.system("clear")
                    selected = number_of_runs
                    print(selected)
                    self.time.sleep(sleeptime)
                    continue
                self.os.system("clear")
                selected -= 1
                print(selected)
                self.time.sleep(sleeptime)
                
            if self.button.enter:
                self.time.sleep(0.5)
                return selected

            if self.button.down:
                self.util.right.on(30, block=False)
                self.util.left.on(30)
                self.time.sleep(0.1)
                self.util.right.on(-30, block=False)
                self.util.left.on(-30)
                self.time.sleep(0.1)

            else:
                self.util.left.off(brake=False)
                self.util.right.off(brake=False)
    
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
        

        """
        exec("self.runs.run"+str(selected)+"()")
        print(str(selected)+" done.")
        """

        return selected + 1







