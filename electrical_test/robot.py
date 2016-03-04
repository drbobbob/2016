#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from wpilib.cantalon import CANTalon

from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp


class MyRobot(wpilib.IterativeRobot):
    
    
    
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        
        self.ball_sensor = Sharp(1)
        
        self.beltmotor = wpilib.CANTalon(6)
        self.pitcher_motor = wpilib.CANTalon(7)
        
        lf_motor = wpilib.CANTalon(2)
        lr_motor = wpilib.CANTalon(3)
        rf_motor = wpilib.CANTalon(4)
        rr_motor = wpilib.CANTalon(5)   
        self.robot_drive = wpilib.RobotDrive(lf_motor, lr_motor,
                                             rf_motor, rr_motor)
        
        #self.tape_motor = wpilib.CANTalon(6)
        #self.winch_motor = wpilib.CANTalon(7)
        
        self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(1)
        
    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.robot_drive.arcadeDrive(self.left_joystick)
        
        # activate the pitcher motor
        if self.left_joystick.getTrigger():
            self.pitcher_motor.set(self.left_joystick.getZ())
        else:
            self.pitcher_motor.set(0)
            
        if self.left_joystick.getRawButton(2):
            self.beltmotor.set(1)
        elif self.left_joystick.getRawButton(3):
            self.beltmotor.set(-1)
        else:
            self.beltmotor.set(0)
    
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)