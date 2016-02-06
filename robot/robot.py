#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

from components.lenny import Lenny
from components.pitcher import Pitcher
from components.tape_measure import Tapemeasure
from components.drive import Drive

class MyRobot(MagicRobot):
    #lenny = Lenny
    #pitcher = Pitcher
    #tapemeasure = Tapemeasure
    drive = Drive
    
    def createObjects(self):
        self.beltmotor = wpilib.CANTalon(0)
        self.sharp = Sharp
        self.pitcher_motor = wpilib.CANTalon(4)
        self.joystick0 = wpilib.Joystick(0)
        self.left_motor = wpilib.CANTalon(2)
        self.right_motor = wpilib.CANTalon(5)
        self.robot_drive = wpilib.RobotDrive(self.left_motor, self.right_motor)
        self.tape_motor = wpilib.CANTalon(6)
        self.winch_motor = wpilib.CANTalon(7)
    def teleopPeriodic(self):
        self.drive.drive(self.joystick0.getX(), self.joystick0.getY())
    
    def autonomous(self):
        pass
        
        
if __name__ == "__main__":
    wpilib.run(MyRobot)