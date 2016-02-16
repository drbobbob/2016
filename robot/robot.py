#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

from components.lenny import Lenny
from components.pitcher import Pitcher
from components.tape_measure import Tapemeasure
from components.drive import Drive

class MyRobot(MagicRobot):
    lenny = Lenny
    pitcher = Pitcher 
    #tapemeasure = Tapemeasure
    drive = Drive
    
    def createObjects(self):
        self.beltmotor = wpilib.CANTalon(3)
        self.ball_sensor = Sharp(1)
        self.pitcher_motor = wpilib.CANTalon(4)
        self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(1)
        self.left_motor = wpilib.CANTalon(2)
        self.right_motor = wpilib.CANTalon(5)  
        self.robot_drive = wpilib.RobotDrive(self.left_motor, self.right_motor)
        #self.tape_motor = wpilib.CANTalon(6)
        #self.winch_motor = wpilib.CANTalon(7)
    
    def teleopInit(self):
        self.pitcher_enabled = False
    
    def teleopPeriodic(self):
        self.drive.tank(self.left_joystick.getY(), self.right_joystick.getY())
        
        # Pitcher controls
        if self.right_joystick.getRawButton(4):
            self.pitcher_enabled = True
        elif self.right_joystick.getRawButton(5):
            self.pitcher_enabled = False
        if self.pitcher_enabled == True:
            self.pitcher.enable()
            
        # Lenny controls
        if self.right_joystick.getTrigger():
            self.lenny.fire()
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
            
    def autonomous(self):
        pass
        
        
if __name__ == "__main__":
    wpilib.run(MyRobot)