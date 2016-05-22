
from magicbot import state, timed_state, AutonomousStateMachine, tunable

from components.drive import Drive
from controllers.angle_controller import AngleController

from controllers.autoaim import AutoAim

class AutoaimBase(AutonomousStateMachine):

    drive = Drive
    angle_ctrl = AngleController
    autoaim = AutoAim
    
    speed = tunable(0.8)
    fwd_tm = tunable(3)

    def initialize(self):
        pass
    
    @state(first=True)
    def drive_forward(self, state_tm):
        self.drive.move_y(self.speed)
        self.angle_ctrl.align_to(0)
        if state_tm > self.fwd_tm:
            self.next_state('turn')
             
        
    @timed_state(duration=4, next_state='fire')
    def turn(self):
        self.angle_ctrl.align_to(self.angle)
        self.autoaim.aim()
      
    @state
    def fire(self):
        self.drive.move_y(0.55)
        self.autoaim.aim()
        


class AutoaimStraight(AutoaimBase):
    
    MODE_NAME = "Autoaim - Straight"
    DEFAULT = True
    
    angle = 0
    
class AutoaimStraightEmpty(AutoaimBase):
    
    MODE_NAME = "Autoaim - Straight Empty"
    DEFAULT = False
    
    angle = 15 # turns right
    speed = tunable(0.7)
    fwd_tm = tunable(1.75)
    

class AutoaimLeft(AutoaimBase):
    
    MODE_NAME = "Autoaim - Start on Left"
    angle = 30 # turns right

class AutoaimRight(AutoaimBase):
    
    MODE_NAME = "Autoaim - Start On Right"
    angle = -30 # turns left
    
