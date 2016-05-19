#!/usr/bin/env python3

import wpilib
from magicbot import MagicRobot
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F, SharpIR2Y0A02

from components.lenny import Lenny
from components.pitcher import Pitcher
from components.drive import Drive

from controllers.angle_controller import AngleController
from controllers.autoaim import AutoAim
from controllers.autolenny import AutoLenny
from controllers.distance_controller import DistanceController
from controllers.position_history import PositionHistory
from controllers.shooter_control import ShooterControl

from networktables.util import ntproperty


class MyRobot(MagicRobot):
    
    # Ordered by expected order of execution
    autolenny = AutoLenny
    autoaim = AutoAim
    shooter_control = ShooterControl
    
    angle_ctrl = AngleController
    distance_ctrl = DistanceController
    pos_history = PositionHistory
    
    lenny = Lenny
    pitcher = Pitcher
    drive = Drive
    
    distance_thing = ntproperty('/teleop/distance_thing', 2)
    
    turn_sensitivity = ntproperty('/teleop/turn_sensitivity', 1)
    fire_toggled = ntproperty('/teleop/fire_toggle', False)
    autoaim_toggled = ntproperty('/teleop/auto_aim_toggle', False)
    autolenny_toggled = ntproperty('/teleop/auto_lenny_toggle', True)
    
    
    ds_ball_in = ntproperty('/teleop/ball_in', False)
    ds_ball_out = ntproperty('/teleop/ball_out', False)
    
    #talon_temp2 = ntproperty('/SmartDashboard/talon_temp/2', 0)
    #talon_temp3 = ntproperty('/SmartDashboard/talon_temp/3', 0)
    #talon_temp4 = ntproperty('/SmartDashboard/talon_temp/4', 0)
    #talon_temp5 = ntproperty('/SmartDashboard/talon_temp/5', 0)
    #talon_temp6 = ntproperty('/SmartDashboard/talon_temp/6', 0)
    #talon_temp7 = ntproperty('/SmartDashboard/talon_temp/7', 0)

    def createObjects(self):
        self.ball_sensor = SharpIRGP2Y0A41SK0F(1)
        self.tower_sensor = SharpIR2Y0A02(0)
        
        self.wheel_encoder = wpilib.Encoder(0, 1, reverseDirection=True)
        
        self.camera_light = wpilib.Relay(1)
        self.camera_light.set(wpilib.Relay.Value.kOn)
        
        self.beltmotor = wpilib.CANTalon(6)
        #self.beltmotor.reverseSensor(True)
        self.beltmotor.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.beltmotor.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.beltmotor.setPID(0.8, 0.05, 0.0, 0.8525, izone=10)
        self.beltmotor.enableBrakeMode(False)
        self.beltmotor.setAllowableClosedLoopErr(10)
        self.beltmotor.configEncoderCodesPerRev(0)

        self.pitcher_motor = wpilib.CANTalon(7)
        self.pitcher_motor.reverseSensor(True)
        self.pitcher_motor.changeControlMode(wpilib.CANTalon.ControlMode.Speed)
        self.pitcher_motor.setFeedbackDevice(wpilib.CANTalon.FeedbackDevice.QuadEncoder)
        self.pitcher_motor.setPID(0.4, 0.05, 0.0, 0.12, izone=10)
        self.pitcher_motor.enableBrakeMode(False)
        self.pitcher_motor.setAllowableClosedLoopErr(10)
        self.pitcher_motor.configEncoderCodesPerRev(0)
        
        self.lf_motor = lf_motor = wpilib.CANTalon(4)
        self.lr_motor = lr_motor = wpilib.CANTalon(5)
        self.rf_motor = rf_motor = wpilib.CANTalon(2)
        self.rr_motor = rr_motor = wpilib.CANTalon(3)

        lf_motor.setInverted(True)
        lr_motor.setInverted(True)
        rf_motor.setInverted(True)
        rr_motor.setInverted(True)
        self.robot_drive = wpilib.RobotDrive(lf_motor, lr_motor,
                                             rf_motor, rr_motor)
        
        self.left_joystick = wpilib.Joystick(0)
        self.right_joystick = wpilib.Joystick(1)
        
        self.move_pos = None
    
    def teleopPeriodic(self):
         
        self.drive.move(self.right_joystick.getX()*self.turn_sensitivity, -self.left_joystick.getY(), True)
        
        # testing: align to absolute angles
        if self.right_joystick.getRawButton(11):
            self.angle_ctrl.align_to(0)
        elif self.right_joystick.getRawButton(10):
            self.angle_ctrl.align_to(179)
        
        # testing: move forward some N
        if self.left_joystick.getRawButton(10):
            if self.move_pos is None:
                self.move_pos = self.distance_ctrl.get_position() + self.distance_thing
            
            self.distance_ctrl.move_to(self.move_pos)
        else:
            self.move_pos = None
        
        # Pitcher controls
        if self.right_joystick.getRawButton(4):
            self.pitcher.enable()
        elif self.right_joystick.getRawButton(5):
            self.pitcher.reverse()
            
        # Lenny controls
        if self.right_joystick.getTrigger() or self.fire_toggled:
            self.shooter_control.fire()
        elif self.right_joystick.getRawButton(2) or self.ds_ball_in:
            self.lenny.ball_in()
        elif self.right_joystick.getRawButton(3) or self.ds_ball_out:
            self.lenny.ball_out()
        elif self.autolenny_toggled:
            self.autolenny.enable()
            
        if self.right_joystick.getRawButton(9):
            self.lenny.ball_shoot()
        
        if self.right_joystick.getRawButton(6) or self.autoaim_toggled:
            self.autoaim.aim()
        
if __name__ == "__main__":
    wpilib.run(MyRobot)
