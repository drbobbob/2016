import wpilib

class Tapemeasure:

    tape_motor = wpilib.CANTalon
    winch_motor = wpilib.CANTalon

    EXTEND = 2
    RETRACT = 3
    STOP = 1
    input = """button input expressed in values 1, 2, and 3"""
    encoderinput = """input from the encoder translated to fit a more simple numeric value"""
    encoderstop1= """quota the encoder must meet to auto-stop the tape measure whilst extended"""

    def execute ( self ):
        """Determines action based on input"""
        if self.encoderinput != self.encoderstop1:
            if self.input == self.RETRACT:
                self.performRetract()
            elif self.input == self.EXTEND:
                self.performExtend()
            else:
                self.performStop ()
        else:
            self.performStop ()
            self.input = 1

    def performExtend (self):
        """activate motors to extend"""
        self.tape_motor.set(0.2)
        self.winch_motor.set(0.2)
    def performRetract (self):
        """activate motors to retract"""
        self.tape_motor.set(-0.2)
        self.winch_motor.set(-0.2)
    def performStop (self):
        """deactivate motors"""
        self.tape_motor.set(0)
        self.winch_motor.set(0)