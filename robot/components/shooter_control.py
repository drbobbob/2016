import wpilib

from .lenny import Lenny
from .pitcher import Pitcher

from networktables.util import ntproperty

class ShooterControl:
    lenny = Lenny
    pitcher = Pitcher
    
    fire_period = ntproperty('/components/shooter_control/fire_period', 1)
    ball_threshold = ntproperty('/components/shooter_control/ball_threshold', 6.7)

    ball_in_speed = ntproperty('/components/shooter_control/ball_in_speed', -0.25)
    shooting = ntproperty('/components/shooter_control/shooting', False)
    
    def __init__(self):
        self.fire_is_happening = False
        self.seen_ball = False
        self.fire_timer = wpilib.Timer()
        self.fire_timer.start()
        
    def fire(self):
        self.pitcher.enable() 
        if self.pitcher.is_ready():
            if self.fire_is_happening == False:
                self.seen_ball = False
            self.fire_is_happening = True
            self.fire_timer.reset()
         
    def execute(self):
        #if fire is called beltmotor and pitcher motor should run for N
        if self.fire_is_happening: 
            ball_out = self.lenny.ball_sensor.getDistance() > self.ball_threshold
            #if not self.seen_ball or not ball_out: 
            self.lenny.ball_in(force=self.ball_in_speed)
            #else:
            #    self.lenny.ball_out()
                
            if not ball_out:
                self.seen_ball = True
            
            self.pitcher.enable()
            if self.fire_timer.hasPeriodPassed(self.fire_period): 
                self.shooting = True
                self.fire_is_happening = False
            else:
                self.shooting = False
        else:
            self.shooting = False
