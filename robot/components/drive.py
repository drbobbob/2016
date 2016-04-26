
import hal
import math
import wpilib

from networktables import NetworkTable
from networktables.util import ntproperty

from robotpy_ext.common_drivers.navx import AHRS

class Drive:
    """
        Controls moving the robot around
    """
    
    robot_drive = wpilib.RobotDrive
    
    # Variables to driver station
    robot_angle = ntproperty('/components/drive/angle', 0)
    robot_pitch = ntproperty('/components/drive/pitch', 0)
    robot_roll = ntproperty('/components/drive/roll', 0)
    robot_x = ntproperty('/components/drive/x', 0)
    robot_y = ntproperty('/components/drive/y', 0)
    
    rotateToAngleRate = ntproperty('/components/drive/pidoutput', 0)
    
    robot_setpoint = ntproperty('/components/drive/setpoint', 0)

    if hal.HALIsSimulation():
        kP = 0.05
        kI = 0.00001
        kD = 0.001
        kF = 0.0
    else:
        kP = 0.05
        kI = 0.00001
        kD = 0.001
        kF = 0.0
        
        

    kToleranceDegrees = 2.0
     
    def __init__(self):
        self.x = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.speed = 0
        self.squared = False
        self.function_called = None

        self.ahrs = AHRS.create_spi()

        turn_controller = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self.ahrs, output=self)
        turn_controller.setInputRange(-180.0,  180.0)
        turn_controller.setOutputRange(-1.0, 1.0)
        turn_controller.setAbsoluteTolerance(self.kToleranceDegrees)
        turn_controller.setContinuous(True)
        self.turn_controller = turn_controller
        
        turn_controller.initTable(NetworkTable.getTable('/components/drive/pid'))
        
    

    def move(self, x, y, squared=False):
        """Moves the robot

        :param x: -1 is left, 1 is right
        :param y: 1 is forward, -1 is backwards

        """
        self.x = x
        self.y = y
        self.squared = squared
        self.function_called = Drive.move
          
    def get_angle(self):
        """Returns the robot's current heading"""
        return self.ahrs.getYaw()
        
    def move_at_angle(self, speed, angle):
        """Moves the robot and turns it to a specified direction"""
        
        self.speed = speed
        self.squared = False
        if abs(angle - self.robot_setpoint) > 0.001:
            self.turn_controller.setSetpoint(angle)
            self.robot_setpoint = angle
        
        self.function_called = Drive.move_at_angle
        
    def is_at_angle(self):
        """
            Returns True if robot is pointing at specified angle. Always
            returns False when move_at_angle is not being called.
        """
        return self.turn_controller.isEnable() and self.turn_controller.onTarget()

    def reset_angle(self):
        self.ahrs.reset()

    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        
        # x: 0.25 to 0.5
        # y: 0.15 to 0.6
        
        # The pure output of the PID controller isn't enough.. 
        # .. need to scale between some min out
        
        # scale between 0 and max
        self.rotateToAngleRate = math.copysign(abs(output)*0.3+0.2, output)

    def execute(self):
        """ JUST DO IT """
        
        if self.function_called == Drive.move_at_angle:
            self.turn_controller.enable()
            if self.turn_controller.onTarget():
                self.x = 0
            else:
                self.x = self.rotateToAngleRate
            self.y = self.speed
            self.squared = False
        else:
            self.turn_controller.disable()
        
        self.robot_drive.arcadeDrive(-self.y, self.x, self.squared)
        
        # send this to the DS
        self.robot_angle = self.get_angle()
        self.robot_x = self.x*self.x if self.squared else self.x
        self.robot_y = self.y*self.y if self.squared else self.y
        self.robot_pitch = self.ahrs.getPitch()
        self.robot_roll = self.ahrs.getRoll()
        
        self.x = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.function_called = None
        self.speed = 0
        self.squared = False
