
from robotpy_ext.autonomous import timed_state, StatefulAutonomous
from components.lenny import Lenny
from components.drive import Drive

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Gallop and Pass'
    drive = Drive
    lenny = Lenny

    def initialize(self):
        pass

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        pass

    @timed_state(duration=3, next_state='pass_ball')              
    def drive_forward(self):
        self.drive.move(0, 1)
        
    @timed_state(duration=3)    
    def pass_ball(self):
        self.lenny.ball_out()