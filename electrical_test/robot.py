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
        pass
        
    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        pass
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)