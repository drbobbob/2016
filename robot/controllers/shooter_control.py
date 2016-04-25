
from components.lenny import Lenny
from components.pitcher import Pitcher

from magicbot import StateMachine, state, timed_state, tunable

class ShooterControl(StateMachine):
    lenny = Lenny
    pitcher = Pitcher
    
    def fire(self):
        self.engage()
        
    def is_firing(self):
        return self.current_state == 'firing'
    
    @state(first=True)
    def prepare_to_fire(self):
        '''Prepares things'''
        self.pitcher.enable()
        
        if self.pitcher.is_ready():
            self.next_state_now('firing')
    
    @timed_state(duration=1, must_finish=True)
    def firing(self):
        '''Fires the ball'''
        
        self.pitcher.enable()
        
        #ball_out = self.lenny.ball_sensor.getDistance() > self.ball_threshold
        
        self.lenny.ball_shoot()
