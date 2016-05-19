
import math

import hal
import wpilib
from magicbot import tunable

from components.drive import Drive
from .my_pid_base import BasePIDComponent

class DistanceController(BasePIDComponent):
    '''
        When enabled, controls the robot's position relative
        to a wheel encoder.
        
        .. warn:: Because this uses a single encoder, if you turn while using
                  this, all bets are off.
    '''
    
    drive = Drive
    wheel_encoder = wpilib.Encoder
    
    wheel_distance = tunable(0)
    ticks_per_ft = tunable(158.3)
    
    if hal.HALIsSimulation():
        kP = 0.01
        kI = 0.0
        kD = 0.0
        kF = 0.0
    else:
        kP = tunable(0.1)
        kI = tunable(0.001)
        kD = tunable(2.0)
        kF = tunable(0.0)
        
    kToleranceFeet = tunable(0.15)
    kIzone = tunable(0.15)
        
    def __init__(self):
        super().__init__(self.get_position, 'distance_ctrl')    
        #self.pid.setOutputRange(-1.0, 1.0)
    
    def get_position(self):
        """Encoder position in feet"""
        return self.wheel_encoder.get() / self.ticks_per_ft
    
    def move_to(self, position):
        self.setpoint = position
        
    def is_at_location(self):
        return self.enabled and \
                abs(self.get_position() - self.setpoint) < self.kToleranceFeet
    
    def pidWrite(self, output):
        rate = math.copysign(abs(output)*0.15+0.45, output)
        super().pidWrite(rate)
    
    def execute(self):
        
        super().execute()
        
        if self.rate is not None:
            if self.is_at_location():
                self.drive.move_y(0)
            else:
                self.drive.move_y(self.rate)
        
        self.wheel_distance = self.get_position()
        
