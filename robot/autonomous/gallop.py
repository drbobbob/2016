
from robotpy_ext.autonomous import timed_state, StatefulAutonomous

from components.drive import Drive

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Drive Forward'
    DEFAULT = True


    drive = Drive

    def initialize(self):
        pass
    
    def on_enable(self):
        StatefulAutonomous.on_enable(self)
        self.drive.reset_angle()

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        pass

    @timed_state(duration=7)
    def drive_forward(self):
        self.drive.move_at_angle(0.8, 0)
