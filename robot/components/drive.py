
import wpilib

from magicbot import tunable

class Drive:
    """
        Controls moving the robot around
    """
    
    robot_drive = wpilib.RobotDrive
    
    robot_x = tunable(0)
    robot_y = tunable(0)
    
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def move(self, x, y, squared=False):
        """
            Moves the robot

            :param x: -1 is left, 1 is right
            :param y: 1 is forward, -1 is backwards
            :param squared: Squares the inputs to make movement more smooth
        """
        if squared:
            self.x = self._square(x)
            self.y = self._square(y)
        else:
            self.x = x
            self.y = y

    def move_x(self, x):
        '''
            Move the robot in the X direction without affecting Y movement.
        
            :param x: -1 is left, 1 is right
        '''
        self.x = x

    def move_y(self, y):
        '''
            Move the robot in the Y direction without affecting X movement.
        
            :param y: -1 is backward, 1 is forward
        '''
        self.y = y

    def _square(self, v):
        if v >= 0.0:
            return v*v
        else:
            return -(v*v)

    def execute(self):
        self.robot_drive.arcadeDrive(-self.y, self.x)
        
        #self.robot_x = self.x
        #self.robot_y = self.y

        self.x = 0.0
        self.y = 0.0

