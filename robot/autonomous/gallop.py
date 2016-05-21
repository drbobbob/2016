
from magicbot import timed_state, AutonomousStateMachine

from components.drive import Drive
from controllers.angle_controller import AngleController

class DriveForward(AutonomousStateMachine):

    MODE_NAME = 'Drive Forward'
    DEFAULT = False


    drive = Drive
    angle_ctrl = AngleController

    def initialize(self):
        pass
    
    @timed_state(duration=2.5, first=True)
    def drive_forward(self):
        self.drive.move_y(1)
        self.angle_ctrl.align_to(0)
