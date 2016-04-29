
""" from robotpy_ext.autonomous import timed_state, StatefulAutonomous

from components.drive import Drive
from components.lenny import Lenny

class CrossAndShoot(StatefulAutonomous):
    
    MODE_NAME = 'Cross And Shoot'
    
    drive = Drive
    lenny = Lenny

    def initialize(self):
        pass
    
    @timed_state(duration= 10, next_state = 'shoot', first = True)
    def drive_straight(self):
        self.drive.move_at_angle(1, 180)
    
    @timed_state(duration = 3)    
    def shoot(self):
        self.lenny.fire() """
        
    
        
        