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
        self.left_motor = wpilib.CANTalon(3)
        self.right_motor = wpilib.CANTalon(4)
        self.robot_drive = wpilib.RobotDrive(self.left_motor, self.right_motor)
        self.joystick = wpilib.Joystick(0)
        
    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.robot_drive.arcadeDrive(self.joystick)
    
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)