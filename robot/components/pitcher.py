
import wpilib 

class Pitcher: 
   
    pitcher_motor = wpilib.CANTalon
    
    def __init__(self):
        self.is_enabled = False
        self.r = 1 
   
    def enable(self):
        """ turn on motor to spin wheel """
        self.is_enabled = True
        
    def disable(self):
        """ turn off motor """
        self.is_enabled = False
        
    def set_range(self, r):
        """ set motor to particular speed? """
        self.r = r
        
    def execute(self):
        """ JUST DO IT """
        #if motor is enabled, set motor to 1#
        #if motor is disabled, set motor to 0#
        if self.is_enabled:
            self.pitcher_motor.set(self.r)
        else:
            self.pitcher_motor.set(0)
            
        self.is_enabled = False
        
        