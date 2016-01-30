
import wpilib 

class Pitcher: 
   
    pitcher_motor = wpilib.CANTalon
   
    def enable(self, is_enabled):
        """ turn on motor to spin wheel """
        self.is_enabled = is_enabled 
        
    def disable(self, is_disabled):
        """ turn off motor """
        self.is_disabled = is_disabled
        
    def set_range(self, r):
        """ set motor to paricular speed? """
        self.r = r
        
    def execute(self):
        """ JUST DO IT ✔ """
        #if motor is enabled, set motor to 1#
        #if motor is disabled, set motor to 0#
        if self.is_enabled:
            self.pitcher_motor.set(1)
        elif self.is_disabled:
            self.pitcher_motor.set(0)
        
    