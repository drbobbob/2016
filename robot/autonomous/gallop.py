
from magicbot import timed_state, AutonomousStateMachine

from components.drive import Drive
from controllers.angle_controller import AngleController

class DriveForward(AutonomousStateMachine):

    MODE_NAME = 'Drive Forward'
    DEFAULT = True


    drive = Drive
    angle_ctrl = AngleController

    def initialize(self):
        pass
    
    def on_enable(self):
        AutonomousStateMachine.on_enable(self)
        self.angle_ctrl.reset_angle()

    @timed_state(duration=2.5, first=True)
    def drive_forward(self):
        self.drive.move_y(1)
        self.angle_ctrl.align_to(0)
