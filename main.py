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
    def MoveWithGyro(self, speed, rot, initial_deg=False, multiplier=0.4, givenBrake=True, timeout=10000):
        initial_rot = self.Avg(self.motorLeft.position, self.motorRight.position)
        
        if not initial_deg:
            initial_deg = self.gyro.angle
        
            
        speed *= -1

        if speed < 0:
            multiplier *= -1
            rot *= -1

        tic = self.time.perf_counter()



        while True:
            #exits if the rot is passed
            if rot < 0 and initial_rot - self.Avg(self.motorLeft.position, self.motorRight.position) > rot * -1 or rot > 0 and self.Avg(self.motorLeft.position, self.motorRight.position) > initial_rot + rot:
                break
            elif self.time.perf_counter() > tic + timeout:
                break
            
            correction = (self.gyro.angle - initial_deg) * multiplier
            print(correction, self.gyro.angle)
            if correction > 99:
                self.steer.on(-100, speed)
                #print("99!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                continue
            elif correction < -99:
                self.steer.on(100, speed)
                #print("-99!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                continue
            self.steer.on(correction, speed)
        self.steer.off(brake=givenBrake)
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
    def TurnToDeg(self, deg, tolerance, motors="ab", divider=4, timeout=10000):
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

    #basic average calculator for two numbers
    def Avg(self, number1, number2):
        sum = number1 + number2
        return sum / 2 
     
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

    def run1(self):
        #gyro reset és preparation
        self.move.gyro.reset()
        self.time.sleep(0.5)
        self.util.left.on(10, brake=True)
        self.util.right.on_for_seconds(10, 1, brake=False)
        self.move.time.sleep(0.5)
        self.util.right.on_for_degrees(-15, 250)
        
        self.move.MoveWithGyro(40, 370, initial_deg=7, multiplier=1.5)
        self.move.TurnToDeg(-360, 270, motors="b")
        self.move.TurnToDeg(-90, 1)
        #self.move.MoveWithGyro(40, 300, initial_deg=-90, multiplier=1)


        self.move.MoveWithGyro(-40, 300, initial_deg=-87+5, givenBrake=False, multiplier=1)
        self.move.MoveWithGyro(-20, 350-20, initial_deg=-90, multiplier=0.8, givenBrake=False)
        self.move.time.sleep(0.7)
        self.move.MoveWithGyro(30, 100, initial_deg=-90, multiplier=1)
        self.move.TurnToDeg(-130, 1)
        self.move.MoveWithGyro(-40, 250, initial_deg=-130, multiplier=1)

        self.move.TurnToDeg(-90, 1, motors="b")
        self.move.MoveWithGyro(-40, 900, initial_deg=-90, multiplier=1, givenBrake=False)
        self.move.MoveWithGyro(-20, 350, initial_deg=-90, multiplier=1, timeout=2)

        self.move.MoveWithGyro(20, 235-5-10, initial_deg=-90, multiplier=1)
        self.move.TurnToDeg(-173, 1, motors="a")

        #rámegy a sortingra
        self.move.MoveWithGyro(3, 30, initial_deg=-180, givenBrake=False, multiplier=2.5)
        self.move.MoveWithGyro(10, 100, initial_deg=-180, givenBrake=False, multiplier=2)
        self.move.MoveWithGyro(10, 300, initial_deg=-180, multiplier=2, timeout=3)

        #felváltva meghajtja a kerekeket, hogy biztos rámenjen
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        
        self.move.MoveWithGyro(90, 100, initial_deg=-220, timeout=1)
        
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        
        self.move.MoveWithGyro(90, 100, initial_deg=-140, timeout=1)
        
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

        #lecsapja a home deliveryt és a vasutat
        self.util.left.on_for_seconds(-40, 2)
        self.move.time.sleep(1.5)
        self.util.left.off()

        #felemeli a kart
        self.util.left.on(100)
        print(self.util.left.state)
        self.move.time.sleep(2)
        print(self.util.left.state)
        self.util.left.off()

        for i in range(4):
            self.util.left.on(100)
            self.move.time.sleep(0.3)
            self.util.left.off()
        
        self.util.left.on(20)
    
        #felemeli a konténereket
        self.util.right.on_for_degrees(-100, 350)

        #előre-hátra mozog, szokott segíteni
        self.move.MoveWithGyro(-40, 10)
        self.move.MoveWithGyro(40, 10)
        self.move.time.sleep(1)

        print(self.util.left.state)
        #tartja a konténereket és hátraindul
        self.util.right.on_for_seconds(-50, 5, block=False)
        self.move.MoveWithGyro(-20, 300)

        self.move.TurnToDeg(-90, 1)
        self.move.MoveWithGyro(40, 1100, initial_deg=-90, multiplier=0.8)

        self.move.TurnToDeg(-135, 1)
        self.move.MoveWithGyro(40, 450, initial_deg=-135, multiplier=0.6, givenBrake=False)
        print(self.util.left.state)
        #fordulás nélkül kanyarodik a jó szögre, gyorsabb
        self.move.MoveWithGyro(40, 1000, initial_deg=-90, multiplier=0.7)


        return

        #elindul
        #self.util.right.on_for_degrees(-20, 50, brake=False)
        self.move.MoveWithGyro(40, 870, initial_deg=5, givenBrake=True, multiplier=0.6)
        self.move.TurnToDeg(45, 1)

        #ledönti a hidat
        self.move.MoveWithGyro(40, 100, initial_deg=45, givenBrake=False, multiplier=0.6)
        self.move.MoveWithGyro(10, 200, initial_deg=70, multiplier=0.6, timeout=3)
        self.move.MoveWithGyro(-20, 200, initial_deg=60)
        self.move.TurnToDeg(50, 1)
        
        #odamegy a sínhez
        self.move.MoveWithGyro(40, 700-5, initial_deg=45, givenBrake=False, multiplier=0.6)
        self.move.MoveWithGyro(40, 345, initial_deg=50, multiplier=0.6)

        #párhuzamosan fordul a vasúti sínre
        self.move.TurnToDeg(75-3, 1, motors="b")
        self.move.TurnToDeg(139-2, 0, motors="a", divider=2)
  
        self.move.time.sleep(0.5)

        #rámegy a sortingra
        self.move.MoveWithGyro(3, 30, initial_deg=139-5, givenBrake=False, multiplier=2.5)
        self.move.MoveWithGyro(10, 100, initial_deg=139, givenBrake=False, multiplier=2)
        self.move.MoveWithGyro(10, 300, initial_deg=139, multiplier=2, timeout=3)

        #felváltva meghajtja a kerekeket, hogy biztos rámenjen
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        
        self.move.MoveWithGyro(90, 100, initial_deg=110, timeout=1)
        
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        
        self.move.MoveWithGyro(90, 100, initial_deg=160, timeout=1)
        
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

        #lecsapja a home deliveryt és a vasutat
        self.util.left.on_for_seconds(-40, 2)
        self.move.time.sleep(1.5)

        #felemeli a kart
        self.util.left.on(100)
        self.move.time.sleep(2)
        
        self.util.left.on(20)

        #felemeli a konténereket
        self.util.right.on_for_degrees(-100, 350)

        #előre-hátra mozog, szokott segíteni
        self.move.MoveWithGyro(-40, 10)
        self.move.MoveWithGyro(40, 10)
        self.move.time.sleep(1)

        #tartja a konténereket és hátraindul
        self.util.right.on_for_seconds(-50, 5, block=False)
        self.move.MoveWithGyro(-20, 300)

        #ledönti a hidat
        self.move.TurnToDeg(222, 1)
        self.move.MoveWithGyro(20, 350+200, initial_deg=222-10, timeout=2.5)
        self.move.MoveWithGyro(-20, 200, initial_deg=222-10)

        #hazajön
        self.move.TurnToDeg(230, 1)
        self.move.MoveWithGyro(40, 1000-250, initial_deg=230, multiplier=0.6)
        self.move.TurnToDeg(180, 1)
        self.move.MoveWithGyro(40, 800-250-100, initial_deg=180, multiplier=0.6, givenBrake=False)
        #fordulás nélkül kanyarodik a jó szögre, gyorsabb
        self.move.MoveWithGyro(40, 1000, initial_deg=230, multiplier=0.7)


    def run2(self):
        self.move.gyro.reset()
        self.time.sleep(0.5)
        
        #motorok helyére húzása
        self.util.left.on_for_seconds(3, 2)
        self.util.right.on_for_seconds(5, 2, block=False)
        
        self.move.MoveWithGyro(-40, 1100-200, initial_deg=5, multiplier = 0.5)
        self.move.MoveWithGyro(-20, 200, initial_deg=0, multiplier = 0.6)

        self.move.steer.on_for_degrees(0, 40, 150)

        #lecsap mindent
        self.util.left.on_for_degrees(-100, 300+100, block=False)
        self.util.right.on_for_degrees(-100, 300)
        
        
        self.move.time.sleep(0.5)
        
        #felemeli a repülőgép oldali kart
        self.util.right.on_for_degrees(40, 500)
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        self.util.right.on_for_degrees(-40, 275-7)
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)

        #kicsit előre megy, felemeli a motort
        self.move.MoveWithGyro(3, 15-5, initial_deg=0.8)
        self.move.MoveWithGyro(20, 60+20-15-10, initial_deg=0, multiplier=0.8)
        self.util.left.on_for_degrees(10, 300)

        #hazajön
        self.move.MoveWithGyro(20, 80-30, initial_deg=0, timeout=2)
        self.move.TurnToDeg(30, 1, motors="a", timeout=3)
        self.move.MoveWithGyro(40, 200-100, initial_deg=30, givenBrake=False)


        #self.move.MoveWithGyro(40, 230, initial_deg=30, multiplier = 0.7)
        self.util.right.on_for_degrees(-40, 100)

        self.move.MoveWithGyro(40, 700, initial_deg=90, multiplier = 0.6)


    def run3(self):
        #! ORSZÁGOS VERSENY (átépített) 
        self.util.left.on(-5)
        self.util.right.on(5)
        self.move.gyro.reset()
        self.time.sleep(0.5)
        
        #rááll az irányra    
        self.move.MoveWithGyro(40, 800, initial_deg=-15, givenBrake=False)
        self.move.MoveWithGyro(40, 130, initial_deg=40)
        self.move.TurnToDeg(30, 1)

        #elmegy a körig
        self.move.drive.on(2, 2)
        self.move.time.sleep(0.3)
        self.move.MoveWithGyro(40, 1000, initial_deg=36, multiplier=0.7)

        #ráfordul
        self.move.TurnToDeg(171, 1)

        #előremegy
        self.move.drive.on(2, 2)
        self.move.time.sleep(0.3)
        self.move.MoveWithGyro(15, 200, initial_deg=171, givenBrake=False, multiplier=1.5)

        #leengedi
        self.util.left.on_for_degrees(20, 160)
        self.move.time.sleep(0.8)

        #hátramegy
        self.move.drive.on(-2, -2)
        self.move.time.sleep(0.3)
        self.move.MoveWithGyro(-20, 50, givenBrake=False)
        self.move.MoveWithGyro(-20, 200, initial_deg=190, multiplier=1, givenBrake=False)
        self.move.MoveWithGyro(-30, 300, initial_deg=170, timeout=3, multiplier=0.8, givenBrake=False)
        self.move.time.sleep(0.5)
        self.move.motorLeft.on(70)
        self.move.time.sleep(1.5)
        self.move.motorLeft.off()


        self.move.time.sleep(0.5)
        self.util.right.on_for_degrees(-60, 40, brake=True)
        self.move.time.sleep(0.3)
        self.util.right.on_for_degrees(10, 50, brake=False)
        self.move.time.sleep(0.5)


        self.move.MoveWithGyro(10, 20, initial_deg=178)
        self.move.TurnToDeg(120-15, 1, motors="b", divider=5)
        self.util.left.on_for_degrees(-50, 160)
        self.move.TurnToDeg(120, 1, motors="a", divider=5)
        self.move.MoveWithGyro(20, 100, initial_deg=120, timeout=3, givenBrake=False)
        self.move.MoveWithGyro(30, 600, initial_deg=127, multiplier=0.8, timeout=2.5)
        self.move.MoveWithGyro(-60, 100, initial_deg=90, givenBrake=False)
     


        """
        self.move.TurnToDeg(-144, 0)
        self.move.drive.on(2, 2)
        self.move.time.sleep(0.3)
        self.move.MoveWithGyro(-40, 950, initial_deg=-144, multiplier=0.7)
        self.move.TurnToDeg(-189, 1)
        self.move.MoveWithGyro(20, 100, initial_deg=-189)
        """
    
        

        #? kék konténer kiengedése ellökéssel
        """
        self.util.right.on_for_degrees(-40, 40, brake=True)
        self.move.time.sleep(0.3)
        self.util.right.on_for_degrees(20, 40, brake=True)
        self.move.time.sleep(1)
        """

        


        


        #* REGIONÁLIS VERSENY
        """
        self.move.gyro.reset()
        self.time.sleep(0.5)
        self.util.right.on(-10)
        self.move.time.sleep(0.5)
        self.util.right.off(brake=True)

        self.move.MoveWithGyro(40, 595+20+20, initial_deg=-4, multiplier=0.6, givenBrake=False)
        
        self.move.time.sleep(0.5)
        #self.move.time.sleep(0.3)
        self.move.TurnToDeg(33, 1, motors="a")
        
        self.move.MoveWithGyro(20, 250-80, initial_deg=33, givenBrake=False, multiplier=0.6)
        
        self.util.right.on_for_degrees(40, 80+80, brake=True)

        self.move.time.sleep(0.5)

        self.move.MoveWithGyro(-40, 100, initial_deg=33, multiplier=0.4)        
        self.move.TurnToDeg(-15, 1, divider=5.5)
        self.move.MoveWithGyro(40, 50, initial_deg=-15, multiplier=0.3+0.4)
        self.move.TurnToDeg(30, 1, divider=5.5)
        self.move.MoveWithGyro(40, 1400-500, initial_deg=33, multiplier=0.75, givenBrake=False)
        self.move.MoveWithGyro(40, 400, initial_deg=35, multiplier=0.75, timeout=3)
        

        #gyroresettől paste
        self.move.gyro.reset()
        self.time.sleep(0.5)
        self.move.MoveWithGyro(-40, 250-70, initial_deg=0)
        self.move.TurnToDeg(-50, 1)
        self.move.MoveWithGyro(20, 500-50, initial_deg=-50, timeout=3)
        
        #teteje -169
        #első kienged -12
        #második kienged 600??? xddd
        #első kidobás

        
        self.move.MoveWithGyro(-40, 100, initial_deg=-50)
        self.move.TurnToDeg(-30, 1, timeout=3)
        self.util.left.on_for_degrees(40, 300)
        

        self.move.TurnToDeg(-100, 1, timeout=2)
        self.move.MoveWithGyro(20, 100, initial_deg=-100)
        self.util.right.on_for_degrees(80, 300-80, brake=True)


        self.move.MoveWithGyro(-25, 200, initial_deg=-100, givenBrake=False, timeout = 2)
        self.move.TurnToDeg(-80-10, 1, timeout=2.5)
        self.move.MoveWithGyro(-40, 500, initial_deg=-80-10-10, givenBrake=False, timeout=4)
  

        self.move.time.sleep(0.5)

        #* Cargo connect kör 
        self.move.MoveWithGyro(40, 100, initial_deg=-140, givenBrake=False)
        self.move.MoveWithGyro(40, 450, initial_deg=-170)
        self.util.left.on_for_degrees(80, 900)
        self.move.time.sleep(0.5)
        self.util.left.on_for_degrees(-50, 850)

        """
        
    
    def run4(self):
        self.move.gyro.reset()
        self.time.sleep(0.5)
        self.util.left.on(3)
        self.util.right.on(-5)
        self.move.MoveWithGyro(60, 1700-400, initial_deg=-1, givenBrake=False)
        self.move.MoveWithGyro(40, 400, initial_deg=-1, timeout=2.5)
        self.move.steer.on(-40, -80)
        self.move.time.sleep(2)
        self.move.steer.off()

        self.move.motorRight.on(-100)
        self.move.time.sleep(1)
        self.move.motorRight.off()

        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        self.util.left.on_for_degrees(-40, 400)
        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        self.util.right.on_for_degrees(100, 2700, block=True)

        """
        tic = self.time.perf_counter()
        while True:
            print(self.util.right.state)
            if self.time.perf_counter() > tic + 3:
                break
        """

        self.spkr.beep(play_type=self.Sound.PLAY_NO_WAIT_FOR_COMPLETE)
        self.util.right.on_for_degrees(-100, 2500, block=False)
        """
        tic = self.time.perf_counter()
        while True:
            print(self.util.right.state)
            if self.time.perf_counter() > tic + 3:
                break
        """
        self.move.time.sleep(0.5)
        #-54 elvileg a merőleges a hídra

        self.move.MoveWithGyro(-20, 230, initial_deg=-54, timeout=2.5)
        self.move.TurnToDeg(40, 1, timeout=2)
        self.move.MoveWithGyro(-20, 100, initial_deg=40)

        self.move.TurnToDeg(90-2, 1)
        self.move.MoveWithGyro(-30, 310+50+30, initial_deg=90-2)
        self.move.TurnToDeg(41-9, 1, motors="a", timeout=2.5)
        
        self.move.MoveWithGyro(-3, 500, initial_deg=41-9, multiplier=0.8)


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
        motorcontrol = False
        motorWiggle = False
        currently_handling = -1
        self.os.system("clear")
        print("Run "+str(selected))
        print("Gyro "+str(self.move.gyro.angle))
        print(self.move.colorSensorMid.color_name)
        while True:
            
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
                    self.util.right.on(3)
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
                selected = 4
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
                self.util.right.off(brake=False)
                self.util.left.off(brake=False)
                manualswitch = True
                break
            elif self.button.down:
                motorcontrol = True
                break
                         
            
                
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
                        
                        if selected == 1 or selected == 0:
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
            
        return None

        """
        exec("self.runs.run"+str(selected)+"()")
        print(str(selected)+" done.")     """








