
import hal

from magicbot import tunable
from components.lenny import Lenny
from .wpi_pid_base import BasePIDComponent


class AutoLenny(BasePIDComponent):
    '''
        Automatically brings balls in when the sensor detects them
    '''

    if hal.HALIsSimulation():
        kP = 0.2
        kI = 0
        kD = 0
        kF = 0
    else:
        kP = 0.2
        kI = 0
        kD = 0
        kF = 0

    kTolerance = tunable(1)

    lenny = Lenny
    
    def __init__(self):
        super().__init__(self._get_lenny, 'autolenny')

        self.pid.setInputRange(0, 40)
        self.pid.setOutputRange(-1.0, 1.0)

    def enable(self):
        '''Call this to enable automatically bringing in the ball'''
        
        self.setpoint = self.lenny.loader_position

    def _get_lenny(self):
        # required because Lenny isn't populated in the constructor
        return self.lenny.get_distance()

    def execute(self):
        
        super().execute()

        if self.rate is not None:
            if abs(self._get_lenny() - self.lenny.loader_position) > self.kTolerance:
                self.lenny.set(self.rate if self.lenny.is_ball_detected() else 0)

