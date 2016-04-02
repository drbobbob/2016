
from robotpy_ext.autonomous import timed_state, StatefulAutonomous
from networktables.util import ntproperty
from components.drive import Drive
from components.shooter_control import ShooterControl
from components.autoaim import AutoAim

class GallopAndLaunch(StatefulAutonomous):

    forward_speed = ntproperty('/autonomous/gallop_and_launch/forward_speed', 0.5)
    angle = ntproperty('/autonomous/gallop_and_launch/angle', 45)
    MODE_NAME = 'Gallop and Launch'
    drive = Drive
    shooter_control = ShooterControl
    
    def initialize(self):
        pass
    
    def on_enable(self):
        StatefulAutonomous.on_enable(self)
        self.drive.reset_angle()

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        pass

    @timed_state(duration=3, next_state='drive_turn')
    def drive_forward(self):
        self.drive.move_at_angle(self.forward_speed, 0)
        
    @timed_state(duration=3, next_state='drive_more')    
    def drive_turn(self):
        self.drive.move_at_angle(0, self.angle)
        
    @timed_state(duration=3, next_state='aim')
    def drive_more(self):
        self.drive.move_at_angle(self.forward_speed, self.angle)

    @timed_state(duration=0, next_state='shoot_ball')
    def aim(self):
        self.autoaim.aim()
    @timed_state(duration=4)    
    def shoot_ball(self):
        self.shooter_control.fire(self, speed=0)
    