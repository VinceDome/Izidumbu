import math, os, time

#a class for all functions that make the robot move using the motors and sensors
class Move:
    from ev3dev2.motor import *
    from ev3dev2.sensor import *
    from ev3dev2.sensor.lego import *
    from ev3dev2.sound import Sound
    from ev3dev2.led import Leds
 
    
    spkr = Sound()
    """
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

    #? IDK the name, new robot
    
    drive = MoveTank(OUTPUT_A, OUTPUT_D)
    steer = MoveSteering(OUTPUT_A, OUTPUT_D)
    motorLeft = Motor(OUTPUT_A)
    motorRight = Motor(OUTPUT_D)

    gyro = GyroSensor(INPUT_1)
    
    colorSensorLeft = ColorSensor(INPUT_2)
    colorSensorRight = ColorSensor(INPUT_3)

    


    def boop(self):
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

    #basic average calculator for two numbers
    def Avg(self, number1, number2):
        sum_ = number1 + number2
        return sum_ / 2 
     
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
    def g(self, speed, rot, initial_deg=False, multiplier=1.5, givenBrake=True, motorsEnd = False, rampup=[0, 0], rampdown=[0, 0], timeout=10000):
        initial_rot = self.Avg(self.motorLeft.position, self.motorRight.position)
        
        if not initial_deg:
            initial_deg = self.gyro.angle
        
        diffU = (speed - rampup[0])
        diffD = (speed - rampdown[0])

        #rampup[0] = honnan rampupol a speedre
        #rampup[1] = hány mp alatt rampupol
        #rampdown[0] = hova rampdownol
        ##rampdown[1] = hány fok alatt rampdownol a végén

  
        _speed = speed

        if speed < 0:
            multiplier *= -1
            rot *= -1

        tic = time.perf_counter()

        

        
        while True:
            #exits if the rot is passed
            if rot < 0 and initial_rot - self.Avg(self.motorLeft.position, self.motorRight.position) > rot * -1 or rot > 0 and self.Avg(self.motorLeft.position, self.motorRight.position) - initial_rot > rot:
                break
            elif time.perf_counter() > tic + timeout:
                break

            if not time.perf_counter() - tic > rampup[1]:
                ratio = (time.perf_counter() - tic) / rampup[1]
                speed = (ratio * diffU) + rampup[0]
                if speed < -100:
                    speed = -100
                elif speed > 100:
                    speed = 100
            else:
                speed = _speed



            if rot < 0 and rampdown[1] != 0:
                remaining = (rot * -1) - (initial_rot - self.Avg(self.motorLeft.position, self.motorRight.position))
                if remaining < rampdown[1]:     
                    ratio = remaining / rampdown[1]
                    speed = (ratio * diffD) + rampdown[0]
                    if speed > -10:
                        speed = -10


            elif rot > 0 and rampdown[1] != 0:
                remaining = rot - (self.Avg(self.motorLeft.position, self.motorRight.position) - initial_rot)
                if remaining < rampdown[1]:
                    ratio = remaining / rampdown[1]
                    speed = (ratio * diffD) + rampdown[0]
                    if speed < 10:
                        speed = 10
           
            
        
            correction = (self.gyro.angle - initial_deg) * multiplier
            #print(correction, self.gyro.angle)

            if correction > 99:
                self.steer.on(100, speed)
                continue
            elif correction < -99:
                self.steer.on(-100, speed)
                continue

            #print(self.gyro.angle, correction, speed)
            self.steer.on(correction, speed)

        if not motorsEnd:
            self.steer.off(brake=givenBrake)
       

        print(self.gyro.angle)

    def t(self, deg, exponent = 1, timeout=10000, motors="ad", givenBrake=True, motorsEnd=False):
        initial_deg = self.gyro.angle

        remaining = deg - self.gyro.angle
        tic = time.perf_counter()
        while remaining != 0:
            if time.perf_counter() > tic + timeout:
                break

            remaining = deg - self.gyro.angle

            remaining = math.copysign(min(abs(remaining) ** exponent, 100), remaining)


            """
            if remaining < 0 and remaining > -3:
                remaining = -3
            elif remaining > 0 and remaining < 3:
                remaining = 3
            """
            if motors == "ad":
                self.drive.on(-remaining, remaining)
            elif motors == "a":
                self.drive.on(-remaining, 0)
            elif motors == "d":
                self.drive.on(0, remaining)

        if motorsEnd:
            self.drive.off(brake=givenBrake)

    '''    
       #turns to a specified angle, but doesn't choose the shortest path
    def t(self, deg, tolerance, motors="ab", timeout=10000):
        
        
        initial_deg = self.gyro.angle
        print("intial", initial_deg)
        print("target", deg)
        
        remaining = deg - self.gyro.angle
        prevgyro = self.gyro.angle
        multiplier = 0.25

        tic = time.perf_counter()
        if initial_deg < deg:
            while remaining != 0 or prevgyro != self.gyro.angle:
                
                print("angle", self.gyro.angle)
                remaining = deg - self.gyro.angle
                print("remaining", remaining)
                
                if time.perf_counter() > tic + timeout:
                    break


                if remaining > 100:
                    if motors == "ab":
                        self.drive.on(-50, 50)
                    elif motors == "a":
                        self.drive.on(-100, 0)
                    elif motors == "b":
                        self.drive.on(0, 100)
                    continue
                
                """
                elif remaining <= 3:
                   break
                elif remaining <= 10:
                    self.drive.on(-7, 7)
                    continue
                """


                #Áron okos: min(kiszámolt szar, 100)
                if motors == "ab":
                    print("driveleft:", remaining *-multiplier, "driveright", {remaining*multiplier})
                    self.drive.on(min(remaining*-multiplier/2, -5), max(remaining*multiplier/2, 5))
                elif motors == "a":
                    self.drive.on(remaining*-multiplier, 0)
                elif motors == "b":
                    self.drive.on(0, remaining*-multiplier)
                prevgyro = self.gyro.angle


        elif initial_deg > deg:
            while self.gyro.angle > deg + tolerance:
                remaining = abs(deg - self.gyro.angle)
                print("angle", self.gyro.angle)
                print("remaining", remaining)
                
                if time.perf_counter() > tic + timeout:
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
                    print("driverigth:", remaining *-multiplier, "driveleft", remaining*multiplier)
                    self.drive.on(remaining*multiplier, remaining*-multiplier)
                elif motors == "a":
                    self.drive.on(remaining*multiplier, 0)
                elif motors == "b":
                    self.drive.on(0, remaining*-multiplier)


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
        if time.perf_counter() > tic + timeout:
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
    '''
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

    topping = Motor(OUTPUT_B)
    lever = Motor(OUTPUT_C)
    

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
            self.move.t(180)
            self.move.g(40, 1427, initial_deg=180)
            self.move.t(0) 

    def run1(self):
        self.move.gyro.reset()
        self.move.time.sleep(0.5)
        
        self.util.lever.on(-40)

        #kitolja
        self.move.g(-80, 1280, initial_deg=0, rampup = [0, 0.5], rampdown=[0, 300], multiplier=1.8)
        self.move.g(40, 150+100, initial_deg=0, rampdown=[0, 50])

        #beáll az ellökő pozícióba
        self.move.t(-50)

        self.util.lever.off()

        self.move.g(40, 350, initial_deg=-50, rampup=[0, 0.5], rampdown=[0, 100])

        #ellöki a kéket
        self.move.t(900, timeout=0.2)
        
        #felemeli a kart és kiüti az energy dolgot
        self.util.lever.on_for_degrees(100, 470, block = False)
        self.move.t(-60, timeout = 0.9)

        #visszaáll, hátramegy, falaz
        self.move.t(-50)
        self.move.g(-30, 250, initial_deg=-45, rampup=[0, 0.5], rampdown=[0, 50])
        self.move.t(-90)
        self.move.g(-30, 300, initial_deg=-90, timeout = 1.5)

        #reset
        self.move.gyro.reset()
        self.move.time.sleep(0.5)

        #ráfordul a sok energyre
        self.move.g(30, 160, initial_deg=0, rampdown=[0, 80])
        self.move.t(-90, motors="d")


        self.util.lever.on_for_degrees(-100, 100, block = False)

        self.move.g(30, 250+50, initial_deg=-90, rampup=[0, 0.5], rampdown=[0, 100])

        self.util.lever.on_for_degrees(100, 250)

        self.util.lever.on_for_degrees(100, 600, block = False)

        self.move.t(-140)
        
        #"""
        self.move.g(-20, 40, initial_deg=-140)

        self.move.t(-90)

        self.move.g(15, 130, initial_deg=-90, multiplier=2)

        self.util.lever.on_for_degrees(-100, 800)
        self.time.sleep(0.5)
        self.util.lever.on_for_degrees(100, 400)

        self.move.g(-30, 300, initial_deg=-90)

        self.util.lever.on_for_degrees(-100, 1000)

        self.move.g(60, 1100, initial_deg=-78, motorsEnd=True, rampup=[0, 0.5])

        self.move.g(60, 300, initial_deg=-95, motorsEnd=True)
        self.util.lever.on_for_degrees(100, 1000, block=False)
        self.move.g(70, 1200, initial_deg=-95, rampup=[60, 0.5])
        #"""

        return
        self.move.t(-86)

        self.move.g(15, 100, initial_deg=-86, multiplier=2)

        self.util.lever.on_for_degrees(-100, 800)
        time.sleep(0.5)
        self.util.lever.on_for_degrees(100, 800, block = False)
        time.sleep(0.5)

        self.move.t(-120)

        self.move.g(-40, 350, initial_deg=-120)
        

        self.util.lever.on_for_degrees(-100, 1000, block=False)

        self.move.t(-92-5)
        
        self.move.g(80, 1500, initial_deg=-92, motorsEnd=True)
        self.util.lever.on_for_degrees(100, 1000, block=False)
        self.move.g(80, 700, initial_deg=-97, givenBrake=False)

    def run2(self):
        self.move.gyro.reset()
        self.move.time.sleep(0.5)

        self.util.lever.on(-40)

        self.util.topping.on(-1)

        self.move.g(-40, 600, initial_deg=0, rampup=[0, 0.8], rampdown = [-20, 100], motorsEnd=True)


        self.move.g(60, 200, rampup = [0, 0.6], rampdown=[0, 60])

        self.move.t(-135)

        self.util.lever.off()

        self.move.g(80, 920, initial_deg=-135, rampup = [0, 0.6], rampdown=[0, 400])

        self.move.t(-225)

        self.move.g(25, 550, initial_deg=-225, multiplier=2, rampdown=[0, 30])
        self.time.sleep(0.8)

        for i in range(2):
            self.move.g(-30, 100, initial_deg=-225, multiplier=2)

            self.move.g(30-15, 200, initial_deg=-225, timeout=1, multiplier=2)
            self.move.time.sleep(0.5)

        self.move.g(-30, 100, initial_deg=-225, motorsEnd=True)
        self.move.g(-60, 550, initial_deg=-260, rampdown=[0, 150])

        self.move.t(-135-20)
        
        """
        

        """
        #kitolja
        self.move.g(-60, 400, initial_deg=-135-20, rampup=[0, 0.5], rampdown=[10, 100])
        self.move.t(-133, motors="a", exponent=1.3)
        self.util.topping.on_for_degrees(20, 200)
        self.time.sleep(0.6)
        self.move.g(-100, 1000, initial_deg=-135-10, rampup=[0, 0.7])

        return
        self.move.t(-55)

        self.move.g(40, 375, initial_deg=-55)

        self.move.t(45)

        self.move.g(80, 800, initial_deg=45, rampup = [0, 0.5])
        self.move.g(-60, 800+150, rampup=[0, 0.5], rampdown = [0, 150], initial_deg=20)


        self.move.t(-38-3, exponent=0.9, timeout=2)

        self.move.g(60, 400-100, initial_deg=-38-3, rampup=[0, 0,5], rampdown=[0, 100])

        self.util.topping.on_for_degrees(50, 200)

        self.time.sleep(0.9)
        
        self.move.g(-80, 150, rampup=[0, 1], motorsEnd=True)
        self.move.g(-80, 1300, initial_deg=-140, rampup=[0, 0.7])

    def run3(self):
        self.move.gyro.reset()
        self.move.time.sleep(0.5)

        self.util.lever.on(-50)

        self.move.g(70, 200, rampup=[0, 0.8], initial_deg=0, motorsEnd=True)

        self.move.g(70, 1230, rampdown=[0, 200], initial_deg=-45, multiplier=0.4)        

        self.move.t(-130, exponent=0.85)

        self.util.lever.off()

        self.move.g(30, 80, rampup=[0, 0.3], rampdown=[0, 30], initial_deg=-130)

        self.util.lever.on_for_degrees(100, 900)

        self.time.sleep(0.7)

        self.util.lever.on_for_degrees(-100, 400, block=False)

        self.move.g(-100, 2000, rampup=[0, 0.8], initial_deg=-180, multiplier=0.7, givenBrake=False)
        #self.move.g(90, 3500, rampup=[0, 1.5], givenBrake=False)

    def run4(self):

        #gyro reset
        self.move.gyro.reset()
        self.move.time.sleep(0.5)
        
        #lehúzza
        self.util.lever.on(-40)
        


        #előremegy
        self.move.g(70, 100, initial_deg=0, rampup=[30, 0.5], motorsEnd=True)
        self.move.g(70, 1650, initial_deg=8, rampdown = [0, 300])

        self.util.lever.off()
        #rááll a falra
        self.move.t(-20, motors="a", motorsEnd=True, timeout=3)
        self.move.g(40, 200, initial_deg=-20, motorsEnd=True)
        self.move.t(-60, motors="a", givenBrake=False, motorsEnd=True)

        #előremegy és elfordul a faltól
        self.move.g(40, 150, initial_deg=-60, rampdown=[0, 50])
        self.move.t(-120, motors="a", exponent=1)

        #előremegy, aztán hirtelen vissza, és ráfordul az egyenesre
        self.move.g(60, 400, initial_deg=-120, motorsEnd=True, rampup=[0, 0.6])
        self.move.g(60, 300, initial_deg=-135)
        self.util.lever.on_for_degrees(100, 350, block=False)

        self.move.g(-60, 200, initial_deg=-120-5, motorsEnd=True)
        self.move.g(-60, 650, initial_deg=-28, multiplier=0.4, rampdown=[0, 200])
        self.move.t(-239)
        self.util.lever.on_for_degrees(-100, 350, block=False)

        #elmegy a missionhöz
        self.move.g(80, 580+10, initial_deg=-239, rampup=[0, 0.7], rampdown = [0, 300], multiplier=1.8)

        #háromszor kart emel
        for i in range(3):
            deg = self.util.lever.position

            while self.util.lever.position < deg + 270:
                self.util.lever.on(100)
                if self.util.lever.is_stalled:
                    print("STALLED")
                    self.util.lever.off()
                    self.time.sleep(0.1)
            self.util.lever.off()


            while self.util.lever.position > deg +5:
                self.util.lever.on(-100)
                if self.util.lever.is_stalled:
                    print("STALLED")
                    self.util.lever.off()
                    self.time.sleep(0.1)
            self.util.lever.off()


        self.move.t(-255, motors="d")
        self.util.lever.on_for_degrees(100, 250, block=False)
        self.move.t(-315, motors="a", timeout=2.5)
        #párhuzamosan ráparkol
        """
        self.move.t(-275, motors="d")
        self.util.lever.on_for_degrees(100, 200+50, block=False)
        self.move.t(-296, motors="a")
        self.move.g(15, 70+20, initial_deg=-296, multiplier=2)
        """
        
        self.util.lever.on_for_degrees(-100, 50+50+10)

        self.move.g(-20, 300, motorsEnd=True)
        self.move.g(-40, 400, initial_deg=-375, givenBrake=False)

        self.move.g(-80, 900, initial_deg=-375, rampup=[-40, -80])

        self.util.lever.on_for_degrees(100, 500)

        """
        #gyro reset
        self.move.gyro.reset()
        self.move.time.sleep(0.5)
        
        #lehúzza
        self.util.lever.on(-100)
        while not self.util.lever.is_stalled:
            pass
        self.util.lever.off()


        #előremegy
        self.move.g(70, 1600, initial_deg=0, rampup=[30, 0.5], rampdown = [0, 300])

        #rááll a falra
        self.move.t(-25, motors="a", motorsEnd=True)
        self.move.g(40, 200, initial_deg=-25, motorsEnd=True)
        self.move.t(-65, motors="a", givenBrake=False, motorsEnd=True)

        #előremegy és elfordul a faltól
        self.move.g(40, 150, initial_deg=-65, rampdown=[0, 50])
        self.move.t(-130, motors="a")

        #előremegy, aztán hirtelen vissza, és ráfordul az egyenesre
        self.move.g(60, 600, initial_deg=-130)
        self.util.lever.on_for_degrees(100, 350, block=False)
        self.move.g(-60, 100, initial_deg=-130, motorsEnd=True)
        self.move.g(-60, 265, initial_deg=-90)
        self.move.t(-246)
        self.util.lever.on_for_degrees(-100, 350, block=False)

        #elmegy a missionhöz
        self.move.g(80, 900, initial_deg=-246, rampdown = [0, 300], multiplier=1.8)

        #háromszor kart emel
        for i in range(3):
            self.util.lever.on_for_degrees(100, 270)
            self.util.lever.on_for_degrees(-100, 270)

        #párhuzamosan ráparkol
        self.move.t(-260, motors="d")
        self.util.lever.on_for_degrees(100, 200, block=False)
        self.move.t(-320, motors="a")

        self.util.lever.on_for_degrees(-100, 50)

        self.move.g(-20, 300, motorsEnd=True)
        self.move.g(-40, 400, initial_deg=-380, givenBrake=False)

        self.move.g(-80, 900, initial_deg=-380, rampup=[-40, -80])

        self.util.lever.on_for_degrees(100, 500)
        
        
        """


    def run5(self):
        #gyro reset
        self.move.gyro.reset()
        self.move.time.sleep(0.5)
        
        self.util.topping.off(brake=False)

        self.move.g(70, 1100, initial_deg=0, rampup=[30, 0.5], rampdown = [0, 250])

        self.move.t(32, exponent=0.8)
       
        self.move.g(40, 500, initial_deg = 32, rampup = [30, 0.5], rampdown=[0, 300], timeout=2)

        #lower the energy units
        self.time.sleep(0.3)
        
        deg = self.util.topping.position

        while self.util.topping.position < deg + 120:
            print(deg, self.util.topping.position)
            self.util.topping.on(10)
            if self.util.topping.is_stalled:
                print("STALLED")
                self.util.topping.off()
                self.time.sleep(0.1)

        self.util.topping.off(brake=False)

        self.time.sleep(0.5)

        self.move.g(-40, 400, initial_deg=32, rampdown=[0, 50])

        #turn to 'The Hand'
        self.move.t(-23)

        self.move.g(80, 1020, initial_deg=-23, rampup=[30, 0.5], rampdown=[10, 300])

        #raise 'The Hand'
        self.move.t(-2, exponent=0.9, timeout=2)

        self.move.time.sleep(0.5)

        self.move.g(-40, 100, initial_deg=0, rampdown=[0, 50])

        #falaz
        self.move.t(-152, exponent=0.8)
        self.move.g(-50, 300, initial_deg=-152)
        self.move.gyro.reset()
        self.move.time.sleep(0.5)

        self.util.lever.on_for_degrees(-100, 500, block=False)

        self.move.g(30, 85, rampup=[0, 0.4], initial_deg=0)
        self.move.t(20, exponent=1.1, motors="d")
        self.move.g(30, 50, initial_deg=20, rampup=[0, 0.5], rampdown=[0, 30], multiplier=2)
        self.move.t(-4-1, exponent=1, motors="a")
        self.move.g(20, 100, initial_deg=-4-1, rampup=[0, 0.5], rampdown=[0, 30], multiplier=2)
        self.util.lever.on_for_degrees(50, 700)

        """
        self.move.g(30, 85)
        self.move.t(20, exponent=0.8, motors="d")
        self.move.g(10, 50)
        self.move.t(-4, exponent=0.8, motors="a")
        self.move.g(10, 100)
        self.util.lever.on_for_degrees(50, 700)
        """


        self.move.g(30, 200, initial_deg=-25)

        self.util.lever.on_for_degrees(-50, 480)
        self.time.sleep(0.5)

        self.move.g(-40, 100, motorsEnd=True)
        self.move.g(-40, 550, initial_deg=30+10, multiplier = 0.3)

        self.move.gyro.reset()
        self.move.time.sleep(0.5)

        self.move.g(40, 100, initial_deg=0, motorsEnd=True, rampup=[0, 0.5])
        self.move.g(40, 700, initial_deg=160, multiplier=0.28, motorsEnd=True)
        self.util.lever.on_for_degrees(-100, 900, block=False)
        self.move.t(190)
        self.move.g(40, 100, initial_deg=190, rampup=[10, 0.5])


        self.move.t(148-2)
        self.move.g(40, 50, initial_deg=148-2, rampup=[10, 0.5])


        deg = self.util.lever.position

        while self.util.lever.position < deg + 1500:
            print(deg, self.util.lever.position)
            self.util.lever.on(100)
            if self.util.lever.is_stalled:
                print("STALLED")
                self.util.lever.off()
                self.time.sleep(0.1)


        self.util.lever.off()



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
        os.system("clear")
        number_of_runs = 5
        self.move.drive.off(brake=False)
        self.util.lever.off(brake=False)
        self.util.topping.off(brake=False)

        time.sleep(0.5)

        previous_selected = 0
        previous_gyro = 0
        selected = default
        manualswitch = False
        motorcontrol = False
        currently_handling = 1
        gyroB = 0

        if default > number_of_runs:
            default=number_of_runs
        def printmenu():
            os.system("clear")
            printed_run = selected

            print("Run "+str(printed_run))
            print("Gyro "+str(self.move.gyro.angle))
    
        def motorpulling():
            if selected == 1:
                self.util.lever.off(brake=False)
                self.util.topping.off(brake=False)
            elif selected == 2:
                self.util.lever.off(brake=False)
                self.util.topping.on(-5)
            elif selected == 3:
                self.util.lever.off(brake=False)
                self.util.topping.off(brake=False)
            elif selected == 4:
                self.util.lever.off(brake=False)
                self.util.topping.off(brake=False)
            if selected == 5:
                self.util.lever.on(20)
                self.util.topping.on(-3)
       
        while True:
            #making the leds red when the gyro is moving
            diff = self.move.gyro.angle-gyroB
            if diff != 0:
                self.both("AMBER")
            else:
                self.both("GREEN")
            gyroB = self.move.gyro.angle


            #selection
            if self.button.right:
                if selected == number_of_runs:
                    selected = 1
                    printmenu()
                    motorpulling()
                    self.time.sleep(sleeptime)
                    continue

                selected += 1
                printmenu()
                motorpulling()
                self.time.sleep(sleeptime)

            if self.button.left:
                if selected == 1:
                    selected = number_of_runs
                    printmenu()
                    motorpulling()
                    self.time.sleep(sleeptime)
                    continue

                selected -= 1
                printmenu()
                motorpulling()
                self.time.sleep(sleeptime)
            
            #motor pulling
            

            #launching runs
            if self.button.enter and not self.button.down:
                self.util.lever.off(brake=False)
                self.util.topping.off(brake=False)
                self.both("ORANGE")
                os.system("clear")
                print("ARMED")
                print(selected)
                
                while self.button.enter:
                    pass

                self.both("RED")

                if selected == 0:
                    print("FAILED")
                    printmenu()
                    motorpulling()
                    continue
                elif selected == 3:
                    self.time.sleep(1.5)
                return selected

            #motorwiggle and motorcontrol launching
            elif self.button.down:
                if self.button.enter:
                    self.util.topping.off(brake=False)
                    self.util.lever.off(brake=False)
                    motorcontrol = True
                    break
                else:
                    self.util.topping.on(50)
                    self.time.sleep(0.1)
                    self.util.topping.on(-50)
                    self.time.sleep(0.1)
                    motorpulling()
                   
            
            
            if selected != previous_selected or previous_gyro != self.move.gyro.angle:
                printmenu()
                motorpulling()
            previous_selected = selected
            previous_gyro = self.move.gyro.angle

        #motorcontrol
        if motorcontrol:
            os.system("clear")
            print("motorCTRL")
            print("right")
            time.sleep(0.5)
            while True:
                if currently_handling == -1:
                    while self.button.left:
                        self.util.topping.on(-20)
                    while self.button.right:
                        self.util.topping.on(20)
                elif currently_handling == 1:  
                    while self.button.left:
                        self.util.lever.on(-100)
                    while self.button.right:
                        self.util.lever.on(100)
                

                if self.button.enter:
                    motorcontrol = False
                    return None
                elif self.button.down:
                    currently_handling *= -1
                    os.system("clear")
                    print("motorCTRL")
                    if currently_handling == -1: 
                        print("left")
                    elif currently_handling == 1: 
                        print("right")
                    time.sleep(0.2)

                self.util.lever.off(brake=False)
                self.util.topping.off(brake=False)

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
            return 5
        return selected+1
            
        

        """
        exec("self.runs.run"+str(selected)+"()")
        print(str(selected)+" done.")     """
