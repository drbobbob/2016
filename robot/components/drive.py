
import wpilib

class Drive:
    """
        Controls moving the robot around
    """
    
    robot_drive = wpilib.RobotDrive
    
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def drive(self, x, y):
        """Moves the robot"""
        self.x = x
        self.y = y
        
    def drive_at_angle(self, speed, angle):
        """Moves the robot and turns it to a specified direction"""
        
        raise NotImplementedError
        
        self.speed = speed
        self.angle = angle
        
    def execute(self):
        """ JUST DO IT """
        
        # for now, ignore driving at a particular angle
        
        self.robot_drive.arcadeDrive(self.y, self.x)
        self.x = 0
        self.y = 0
    