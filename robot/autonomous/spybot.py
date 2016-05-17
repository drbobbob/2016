'''
Created on Apr 28, 2016

@author: Yasmine
'''

from robotpy_ext.autonomous import timed_state, state, StatefulAutonomous
from networktables.util import ntproperty
from components.drive import Drive
from controllers.shooter_control import ShooterControl
from controllers.autoaim import AutoAim
from controllers.angle_controller import AngleController

class Spybot(StatefulAutonomous):

    forward_speed = ntproperty('/autonomous/spybot/forward_speed', 0.5)
    angle = ntproperty('/autonomous/spybot/angle', 45)
    # Variables from camera
    present = ntproperty('/components/autoaim/present', False)
    MODE_NAME = 'Spybot'
    
    drive = Drive
    shooter_control = ShooterControl
    angle_ctrl = AngleController
    
    def initialize(self):
        pass
    
    def on_enable(self):
        StatefulAutonomous.on_enable(self)
        self.angle_ctrl.reset_angle()

    @state(first=True)
    def drive_forward(self):
        self.angle_ctrl.align_to(0)
        self.drive.move_y(self.forward_speed)
        if self.present:
            self.next_state('aim_and_shoot')
        
        
    @timed_state(duration=4)    
    def aim_and_shoot(self):
        self.autoaim.aim()
    