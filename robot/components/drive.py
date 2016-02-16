
import wpilib

class Drive:
    """
        Controls moving the robot around
    """
    
    robot_drive = wpilib.RobotDrive
     
    def __init__(self):
        self.x = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.function_called = None
        
    def move(self, x, y):
        """Moves the robot"""
        self.x = x
        self.y = y
        self.function_called = Drive.move
        
    def tank(self, y1, y2): 
        self.y1 = y1
        self.y2 = y2 
        self.function_called = Drive.tank
        
    def move_at_angle(self, speed, angle):
        """Moves the robot and turns it to a specified direction"""
        
        raise NotImplementedError
        
        self.speed = speed
        self.angle = angle
        
    def execute(self):
        """ JUST DO IT """
        
        # for now, ignore driving at a particular angle
        
        if self.function_called == Drive.tank:  
            self.robot_drive.tankDrive(self.y1, self.y2)
        else: 
            self.robot_drive.arcadeDrive(self.y, self.x)
        
        self.x = 0
        self.y = 0
        self.y1 = 0
        self.y2 = 0
        self.function_called = None
        