#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from wpilib.cantalon import CANTalon

class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.stick1 = wpilib.Joystick(1)
        self.stick2 = wpilib.Joystick(2)
        self.motor1 = wpilib.CANTalon(1)
        self.motor2 = wpilib.CANTalon(2)
        
    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        y = self.stick1.getY()
        self.motor1.set(y)
        
        x = self.stick2.getY()
        self.motor2.set(x)
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)