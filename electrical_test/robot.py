#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from wpilib.cantalon import CANTalon

from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F, SharpIR2Y0A02

from networktables.util import ntproperty

class MyRobot(wpilib.IterativeRobot):
    
    belt = ntproperty('/belt', 0)
    
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        
        self.ball_sensor = SharpIRGP2Y0A41SK0F(0)
        self.tower_sensor = SharpIR2Y0A02(1)
        
        self.camera_light = wpilib.Relay(1)
        
        self.beltmotor = wpilib.CANTalon(6)
        self.beltmotor.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.beltmotor.configEncoderCodesPerRev(0)
        
        self.pitcher_motor = wpilib.CANTalon(7)
        self.pitcher_motor.reverseSensor(True)
        self.pitcher_motor.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
        #self.pitcher_motor.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.pitcher_motor.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        #self.pitcher_motor.setPID(0.4, 0.05, 0.0, 0.12, izone=10)
        #self.pitcher_motor.enableBrakeMode(False)
        #self.pitcher_motor.setAllowableClosedLoopErr(10)
        #self.pitcher_motor.configEncoderCodesPerRev(0)
        
        lf_motor = wpilib.CANTalon(4)
        lr_motor = wpilib.CANTalon(5)
        rf_motor = wpilib.CANTalon(2)
        rr_motor = wpilib.CANTalon(3)

        lf_motor.setInverted(True)
        lr_motor.setInverted(True)
        rf_motor.setInverted(True)
        rr_motor.setInverted(True)
        self.robot_drive = wpilib.RobotDrive(lf_motor, lr_motor,
                                             rf_motor, rr_motor)
        
        # tapemeasure stuff.. 
        #self.tape_motor = wpilib.CANTalon(6)
        #self.winch_motor = wpilib.CANTalon(7)
        
        #self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(0)
        
    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.robot_drive.arcadeDrive(self.right_joystick)
        
        self.belt = self.beltmotor.getEncVelocity()
        
        # activate the pitcher motor
        if self.right_joystick.getTrigger():
            self.pitcher_motor.set(self.right_joystick.getZ())
        else:
            self.pitcher_motor.set(0)
            
        if self.right_joystick.getRawButton(2):
            self.beltmotor.set(1)
        elif self.right_joystick.getRawButton(3):
            self.beltmotor.set(-1)
        else:
            self.beltmotor.set(0)
    
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)