

import wpilib

class Tapemeasure:
    '''we will need electric actuator or pnuematic piston. piston will have solenoid and pid pressure system.
    this system will control gear box for wench '''
    
    EXTEND = 3
    RETRACT = 2
    STOP = 1
    input = STOP
    lastinput = STOP
    encoderinput = derp
    encoderstop= bler
    def update ( self, input ):
        """updates inputs and remembers last input"""
        self.lastinput = self.input
        self.input = input

    def perform ( self ):
        """Determines action based on last input"""
        if self.input != self.lastinput:
            if self.encoderinput != self.encoderstop:
                if self.input == self.STOP:
                    self.performStop()
                    self.performExtend()
                elif self.input == self.RETRACT:
                    self.performRetract()
                elif self.input == self.EXTEND:
                    self.performExtend()

    def performExtend (self):
        """activate motors to extend"""
    def performRetract (self):
        """activate motors to retract"""
    def performStop (self):
        """deactivate motors"""