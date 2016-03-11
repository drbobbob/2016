
from robotpy_ext.autonomous import timed_state, StatefulAutonomous

from components.drive import Drive

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'Drive Forward'


    drive = Drive

    def initialize(self):
        pass

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        pass

    @timed_state(duration=3)
    def drive_forward(self):
        self.drive.move(0, 1)
