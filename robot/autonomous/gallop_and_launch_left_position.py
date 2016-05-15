from magicbot import timed_state, AutonomousStateMachine
from networktables.util import ntproperty
from components.drive import Drive
from controllers.shooter_control import ShooterControl
from controllers.angle_controller import AngleController

class GallopAndLaunchleft(AutonomousStateMachine):

    forward_speed = ntproperty('/autonomous/gallop_and_launch/forward_speed', 0.5)
    angle = ntproperty('/autonomous/gallop_and_launch/angle', -45)
    MODE_NAME = 'Gallop and Launch Left'
    
    angle_ctrl = AngleController
    drive = Drive
    shooter_control = ShooterControl
    
    def initialize(self):
        pass
    
    def on_enable(self):
        AutonomousStateMachine	.on_enable(self)
        self.angle_ctrl.reset_angle()

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        pass

    @timed_state(duration=3, next_state='drive_turn')
    def drive_forward(self):
        self.angle_ctrl.align_to(0)
        self.drive.move_y(self.forward_speed)
        
    @timed_state(duration=3, next_state='drive_more')    
    def drive_turn(self):
        self.angle_ctrl.align_to(self.angle)
        
    @timed_state(duration=3, next_state='shoot_ball')
    def drive_more(self):
        self.angle_ctrl.align_to(self.angle)
        self.drive.move_y(self.forward_speed)
        
    @timed_state(duration=4)    
    def shoot_ball(self):
        self.shooter_control.fire()
    