#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F, SharpIR2Y0A02

from components.autoaim import AutoAim
from components.lenny import Lenny
from components.pitcher import Pitcher
#from components.tape_measure import Tapemeasure
from components.drive import Drive
from components.shooter_control import ShooterControl

from networktables.util import ntproperty

class MyRobot(MagicRobot):
    
    auto_aim = AutoAim
    shooter_control = ShooterControl
    lenny = Lenny
    pitcher = Pitcher
    #tapemeasure = Tapemeasure
    drive = Drive
    
    use_arcade_drive = ntproperty('/SmartDashboard/use_arcade', True, True)
    fire_toggled = ntproperty('/teleop/fire_toggle', False, True)
    lenny_toggled = ntproperty('/teleop/lenny_toggle', False, True) 

    def createObjects(self):
        self.ball_sensor = SharpIRGP2Y0A41SK0F(0)
        self.tower_sensor = SharpIR2Y0A02(1)
        
        self.camera_light = wpilib.Relay(0)
        
        self.beltmotor = wpilib.CANTalon(6)
        self.pitcher_motor = wpilib.CANTalon(7)
        self.pitcher_motor.reverseSensor(True)
        self.pitcher_motor.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.pitcher_motor.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.pitcher_motor.setPID(0.4, 0.05, 0.0, 0.12, izone=10)
        self.pitcher_motor.enableBrakeMode(False)
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
        
        # tapemeasure stuff.. 
        #self.tape_motor = wpilib.CANTalon(6)
        #self.winch_motor = wpilib.CANTalon(7)
        
        self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(1)
    
    def teleopInit(self):
        self.pitcher_enabled = False
    
    def teleopPeriodic(self):
        
        # NOTE: minimum stationary turn power is ~0.7
        
        if self.use_arcade_drive:
            self.drive.move(self.right_joystick.getX(), -self.right_joystick.getY())
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
        if self.right_joystick.getTrigger() or self.fire_toggled:
            self.shooter_control.fire()
        elif self.left_joystick.getRawButton(2) or self.lenny_toggled:
            self.lenny.ball_in()
        elif self.right_joystick.getRawButton(3):
            self.lenny.ball_out()
            
            
        if self.left_joystick.getTrigger():
            self.auto_aim.aim(-self.right_joystick.getY())
        
        # TODO: This needs to be controlled by the autoaim class, or via networktables
        if self.right_joystick.getRawButton(9):
            self.camera_light.set(wpilib.Relay.Value.kOn)
        else:
            self.camera_light.set(wpilib.Relay.Value.kOff)
        
        # Tapemeasure controls
        #if self.left_joystick.getRawButton(6):
            #self.tapemeasure.extend()
        #elif self.left_joystick.getRawButton(7):
            #self.tapemeasure.retract()
        # if self.left_joystick.getTrigger():
            #self.drive.move_at_angle(0, 90)
        
if __name__ == "__main__":
    wpilib.run(MyRobot)