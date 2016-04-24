
from .lenny import Lenny
from .pitcher import Pitcher

from magicbot import StateMachine, state, timed_state, tunable

class ShooterControl(StateMachine):
    lenny = Lenny
    pitcher = Pitcher
    
    ball_in_speed = tunable(-500)
        
    def fire(self):
        self.begin()
    
    @state(first=True)
    def prepare_to_fire(self):
        '''Prepares things'''
        self.pitcher.enable()
        
        # TODO: want to call next thing immediately?
        if self.pitcher.is_ready():
            self.next_state_now('firing')
        else:
            self.done()
    
    # TODO: really want a 'run at least' state thing
    
    @timed_state(duration=1)
    def firing(self):
        '''Fires the ball'''
        
        self.pitcher.enable()
        
        #ball_out = self.lenny.ball_sensor.getDistance() > self.ball_threshold
        
        self.lenny.ball_in(force=self.ball_in_speed, pid=True)
