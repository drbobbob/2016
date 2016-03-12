
import hal
import wpilib

from networktables.util import ntproperty

from robotpy_ext.common_drivers.navx import AHRS

class Drive:
    """
        Controls moving the robot around
    """
    
    robot_drive = wpilib.RobotDrive
    
    # Variables to driver station
    robot_angle = ntproperty('/components/drive/angle', 0)
    robot_setpoint = ntproperty('/components/drive/setpoint', 0)
    
    max_turn = ntproperty('/components/drive/max_turn', 0.85)

    if hal.HALIsSimulation():
        kP = 0.3
    else:
        kP = 0.05
        
    kI = 0.00
    kD = 0.00
    kF = 0.00

    kToleranceDegrees = 2.0
     
    def __init__(self):
        self.x = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.speed = 0
        self.rotateToAngleRate = 0
        self.function_called = None

        self.ahrs = AHRS.create_spi()

        turn_controller = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self.ahrs, output=self)
        turn_controller.setInputRange(-180.0,  180.0)
        turn_controller.setOutputRange(-1.0, 1.0)
        turn_controller.setAbsoluteTolerance(self.kToleranceDegrees)
        turn_controller.setContinuous(True)
        self.turn_controller = turn_controller

    def move(self, x, y):
        """Moves the robot

        :param x: -1 is left, 1 is right
        :param y: 1 is forward, -1 is backwards

        """
        self.x = x
        self.y = y
        self.function_called = Drive.move
        
    def tank(self, y1, y2): 
        self.y1 = y1
        self.y2 = y2 
        self.function_called = Drive.tank
        
    def get_angle(self):
        """Returns the robot's current heading"""
        return self.ahrs.getYaw()
        
    def move_at_angle(self, speed, angle):
        """Moves the robot and turns it to a specified direction"""
        
        self.speed = speed
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
        self.rotateToAngleRate = output

    def execute(self):
        """ JUST DO IT """
        
        if self.function_called == Drive.move_at_angle:
            self.turn_controller.enable()
            self.robot_drive.arcadeDrive(-self.speed, max(min(self.rotateToAngleRate, self.max_turn), -self.max_turn))
        else:
            self.turn_controller.disable()

            if self.function_called == Drive.tank:
                self.robot_drive.tankDrive(self.y1, self.y2)

            else:
                self.robot_drive.arcadeDrive(-self.y, max(min(self.x, self.max_turn), -self.max_turn))
        
        # send this to the DS
        self.robot_angle = self.get_angle()
        
        self.x = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.function_called = None
        self.speed = 0
