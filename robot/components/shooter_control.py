import wpilib

from .lenny import Lenny
from .pitcher import Pitcher

from networktables.util import ntproperty

class ShooterControl:
    lenny = Lenny
    pitcher = Pitcher
    
    fire_period = ntproperty('/components/shooter_control/fire_period', 1)
    
    def __init__(self):
        self.fire_is_happening = False
        self.fire_timer = wpilib.Timer()
        self.fire_timer.start()
        
    def fire(self):
        self.pitcher.enable() 
        if self.pitcher.is_ready():
            self.fire_is_happening = True
            self.fire_timer.reset()
         
    def execute(self):
        #if fire is called beltmotor and pitcher motor should run for N
        if self.fire_is_happening:  
            self.lenny.ball_in(force=True)
            self.pitcher.enable()
            if self.fire_timer.hasPeriodPassed(self.fire_period): 
                self.fire_is_happening = False