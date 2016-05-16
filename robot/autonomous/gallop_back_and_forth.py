from magicbot import timed_state, AutonomousStateMachine

from components.drive import Drive
from controllers.angle_controller import AngleController

class GallopBackAndForth(AutonomousStateMachine):

    MODE_NAME = 'Gallop Back and Forth'

    angle_ctrl = AngleController
    drive = Drive

    def initialize(self):
        pass
    
    def on_enable(self):
        AutonomousStateMachine.on_enable(self)
        self.angle_ctrl.reset_angle()

    @timed_state(duration=1.7, next_state="drive_backward", first=True)
    def drive_forward(self):
        self.drive.move_y(1)
        self.angle_ctrl.align_to(0)
        
    @timed_state(duration=1.7)
    def drive_backward(self):
        self.drive.move_y(-1)
        self.angle_ctrl.align_to(0)
