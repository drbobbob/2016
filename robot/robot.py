
import wpilib
from magicbot import MagicRobot
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

import components.lenny.Lenny
import components.pitcher.Pitcher
import components.TapMes.Tapemeasure
import components.drive.Drive
from components.drive import Drive

class MyRobot(MagicRobot):
    lenny = components.lenny.Lenny
    pitcher = components.pitcher.Pitcher
    tapemeasure = components.TapMes.Tapemeasure
    drive = components.drive.Drive
    
    def createObjects(self):
        self.beltmotor = wpilib.CANTalon(0)
        self.sharp = Sharp
        self.pitcher_motor = wpilib.CANTalon(1)
        self.motor_r = wpilib.CANTalon(2)
        self.motor_l = wpilib.CANTalon(3)
        self.joystick0 = wpilib.Joystick(0)
        
    def teleopPeriodic(self):
        self.drive(self.joystick0.getX(), self.joystick0.getY())
    
    def autonomous(self):
        pass
        