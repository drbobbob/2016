import wpilib

class Tapemeasure:
    EXTEND = 3
    RETRACT = 2
    STOP = 1
    input = """button input expressed in values 1, 2, and 3"""
    lastinput = """Current input for action"""
    encoderinput = """input from the encoder translated to fit a more simple numeric value"""
    encoderstop1= """quota the encoder must meet to auto-stop the tape measure whilst extended"""
    encoderstop2 = """the default state of the encoder/motors"""
    def update ( self, input ):
        """updates inputs and remembers last input"""
        self.lastinput = self.input
        self.input = input

    def perform ( self ):
        """Determines action based on last input"""
        if self.encoderinput != self.encoderstop1:
            if self.input != self.lastinput:
                if self.input == self.RETRACT:
                    self.performRetract()
                elif self.input == self.EXTEND:
                    self.performExtend()
                else:
                    self.performStop ()
        else:
                self.performStop ()

    def performExtend (self):
        """activate motors to extend"""

    def performRetract (self):
        """activate motors to retract"""

    def performStop (self):
        """deactivate motors"""
