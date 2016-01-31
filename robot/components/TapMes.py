import wpilib

class Tapemeasure:
    EXTEND = 3
    RETRACT = 2
    STOP = 1
    input = STOP
    lastinput = STOP
    def update ( self, input ):
        """updates inputs and remembers last input"""
        self.lastinput = self.input
        self.input = input

    def perform ( self ):
        """Determines action based on last input"""
        if self.input != self.lastinput:
            if self.input == self.EXTEND:
                self.performExtend()
            elif self.input == self.RETRACT:
                self.performRetract()
            elif self.input == self.STOP:
                self.performStop()

    def performExtend (self):
        """activate motors to extend"""
    def performRetract (self):
        """activate motors to retract"""
    def performStop (self):
        """deactivate motors"""