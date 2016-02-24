#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

from components.lenny import Lenny
from components.pitcher import Pitcher
from components.tape_measure import Tapemeasure
from components.drive import Drive
from components.shooter_control import ShooterControl

from networktables.util import ntproperty

class MyRobot(MagicRobot):
    shooter_control = ShooterControl
    lenny = Lenny
    pitcher = Pitcher 
    #tapemeasure = Tapemeasure
    drive = Drive
    
    use_arcade_drive = ntproperty('/SmartDashboard/use_arcade', True, True)
    
    def createObjects(self):
        self.ball_sensor = Sharp(0)
        
        self.beltmotor = wpilib.CANTalon(6)
        self.pitcher_motor = wpilib.CANTalon(7)
        self.pitcher_motor.reverseSensor(True)
        self.pitcher_motor.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.pitcher_motor.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.pitcher_motor.setPID(0.4, 0.05, 0.0, 0.12, izone=10)
        self.pitcher_motor.enableBrakeMode(True)
        self.pitcher_motor.setAllowableClosedLoopErr(10)
        self.pitcher_motor.configEncoderCodesPerRev(0)
        
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
        
        #self.tape_motor = wpilib.CANTalon(6)
        #self.winch_motor = wpilib.CANTalon(7)
        
        self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(1)
    
    def teleopInit(self):
        self.pitcher_enabled = False
    
    def teleopPeriodic(self):
        if self.use_arcade_drive:
            self.drive.move(self.left_joystick.getX(), self.left_joystick.getY())
        else:
            self.drive.tank(self.left_joystick.getY(), self.right_joystick.getY())
        
        # Pitcher controls
        if self.right_joystick.getRawButton(4):
            self.pitcher_enabled = True
        elif self.right_joystick.getRawButton(5):
            self.pitcher_enabled = False
        if self.pitcher_enabled == True:
            self.pitcher.enable()
            self.pitcher_enabled = False
            
        # Lenny controls
        if self.right_joystick.getTrigger():
            self.shooter_control.fire()
        elif self.left_joystick.getRawButton(2):
            self.lenny.ball_in()
        elif self.left_joystick.getRawButton(3):
            self.lenny.ball_out()
            
        # Tapemeasure controls
        #if self.left_joystick.getRawButton(6):
            #self.tapemeasure.extend()
        #elif self.left_joystick.getRawButton(7):
            #self.tapemeasure.retract()
        # if self.left_joystick.getTrigger():
            #self.drive.move_at_angle(0, 90)
        
if __name__ == "__main__":
    wpilib.run(MyRobot)