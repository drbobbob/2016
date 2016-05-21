
from magicbot import state, timed_state, AutonomousStateMachine, tunable

from components.drive import Drive
from controllers.angle_controller import AngleController

from controllers.autoaim import AutoAim

class AutoaimBase(AutonomousStateMachine):

    drive = Drive
    angle_ctrl = AngleController
    autoaim = AutoAim
    
    speed = tunable(0.8)

    def initialize(self):
        pass
    
    @timed_state(duration=2, first=True, next_state='turn')
    def drive_forward(self):
        self.drive.move_y(self.speed)
        self.angle_ctrl.align_to(0)
        
    @timed_state(duration=4, next_state='fire')
    def turn(self):
        self.angle_ctrl.align_to(self.angle)
        self.autoaim.aim()
      
    @state
    def fire(self):
        self.autoaim.aim()
        


class AutoaimStraight(AutoaimBase):
    
    MODE_NAME = "Autoaim - Straight"
    DEFAULT = True
    
    angle = 0
    
class AutoaimStraightEmpty(AutoaimBase):
    
    MODE_NAME = "Autoaim - Straight Empty"
    DEFAULT = False
    
    angle = 0
    speed = tunable(0.7)
    

class AutoaimLeft(AutoaimBase):
    
    MODE_NAME = "Autoaim - Start on Left"
    angle = 30 # turns right

class AutoaimRight(AutoaimBase):
    
    MODE_NAME = "Autoaim - Start On Right"
    angle = -30 # turns left
    
