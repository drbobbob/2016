
import wpilib

from robotpy_ext.common_drivers.navx import AHRS

class Drive:
    """
        Controls moving the robot around
    """
    
    robot_drive = wpilib.RobotDrive

    kP = 0.5
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
        self.turn_controller.setSetpoint(angle)
        self.function_called = Drive.move_at_angle

    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        self.rotateToAngleRate = output

    def execute(self):
        """ JUST DO IT """
        
        if self.function_called == Drive.move_at_angle:
            self.turn_controller.enable()
            self.robot_drive.arcadeDrive(-self.speed, self.rotateToAngleRate)
        else:
            self.turn_controller.disable()

            if self.function_called == Drive.tank:
                self.robot_drive.tankDrive(self.y1, self.y2)

            else:
                self.robot_drive.arcadeDrive(-self.y, self.x)
        
        self.x = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.function_called = None
        self.speed = 0