
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
    target_height_setpoint = ntproperty('/components/drive/target_height_setpoint', 3)
    target_height = ntproperty('/components/autoaim/target_height', 0)

    if hal.HALIsSimulation():
        kP = 0.1
        kHeightP = 0.1
    else:
        kP = 0.1
        kHeightP = 0.1
        
    kI = 0.00
    kD = 0.00
    kF = 0.00

    kHeightI = 0.00
    kHeightD = 0.00
    kHeightF = 0.00

    kToleranceDegrees = 2.0
    kToleranceHeight = 0.1
     
    def __init__(self):
        self.x = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.speed = 0
        self.rotateToAngleRate = 0
        self.move_to_target_height_rate = 0
        self.function_called = None
        self.last_function_called = None

        self.ahrs = AHRS.create_spi()

        turn_controller = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self.ahrs, output=self)
        turn_controller.setInputRange(-180.0,  180.0)
        turn_controller.setOutputRange(-1.0, 1.0)
        turn_controller.setAbsoluteTolerance(self.kToleranceDegrees)
        turn_controller.setContinuous(True)
        self.turn_controller = turn_controller
        
        height_controller = wpilib.PIDController(self.kHeightP, self.kHeightI, self.kHeightD, self.kHeightF, self.get_target_height, output=self.pid_move_to_target_height_write)
        height_controller.setInputRange(0,  7)  # 1-7 feet
        height_controller.setOutputRange(-1.0, 1.0)
        height_controller.setAbsoluteTolerance(self.kToleranceHeight)
        height_controller.setContinuous(False)
        self.height_controller = height_controller

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

    def get_target_height(self):
        """Returns the target height from the camera vision code"""
        return self.target_height

        
    def move_at_angle(self, speed, angle):
        """Moves the robot and turns it to a specified direction"""
        
        self.speed = speed
        if abs(angle - self.robot_setpoint) > 0.001:
            self.turn_controller.setSetpoint(angle)
            self.robot_setpoint = angle
        
        self.function_called = Drive.move_at_angle

    def move_to_target(self, angle = 0):
        """
            Moves the robot to the proper distance from the 
            target and turns the robot to a specified direction
        """
        if abs(angle - self.robot_setpoint) > 0.001:
            self.turn_controller.setSetpoint(angle)
            self.robot_setpoint = angle

        # If robot just started autoaim then reset the setpoint
        if self.last_function_called is not Drive.move_to_target:
            self.height_controller.setSetpoint(self.target_height_setpoint)
        
        self.function_called = Drive.move_to_target

        
    def is_at_angle(self):
        """
            Returns True if robot is pointing at specified angle. Always
            returns False when the turn controller is disabled.
        """
        return self.turn_controller.isEnable() and self.turn_controller.onTarget()

    def is_at_target_height(self):
        """
            Returns True if robot camera is at correct target height. Always
            returns False when the height controller is disabled.
        """
        return self.height_controller.isEnable() and self.height_controller.onTarget()


    def reset_angle(self):
        self.ahrs.reset()

    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        self.rotateToAngleRate = output


    def pid_move_to_target_height_write(self, output):
        self.move_to_target_height_rate = output

    def execute(self):
        """ JUST DO IT """
        if self.function_called == Drive.move_to_target:
            self.turn_controller.enable()
            self.height_controller.enable()
            self.robot_drive.arcadeDrive(-self.move_to_target_height_rate, self.rotateToAngleRate)
        elif self.function_called == Drive.move_at_angle:
            self.turn_controller.enable()
            self.height_controller.disable()
            self.robot_drive.arcadeDrive(-self.speed, self.rotateToAngleRate)
        else:
            self.turn_controller.disable()
            self.height_controller.disable()
            if self.function_called == Drive.tank:
                self.robot_drive.tankDrive(self.y1, self.y2)

            else:
                self.robot_drive.arcadeDrive(-self.y, self.x)
        
        # send this to the DS
        self.robot_angle = self.get_angle()
        
        self.x = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.last_function_called = self.function_called
        self.function_called = None
        self.speed = 0
