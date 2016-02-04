
import wpilib
from magicbot import MagicRobot
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

from components.lenny import Lenny
import components.pitcher.Pitcher
from components.tape_measure import Tapemeasure
from components.drive import Drive

class MyRobot(MagicRobot):
    lenny = Lenny
    pitcher = components.pitcher.Pitcher
    tapemeasure = Tapemeasure
    drive = Drive
    
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
        