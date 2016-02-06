import wpilib

class Tapemeasure:

    tape_motor = wpilib.CANTalon
    winch_motor = wpilib.CANTalon

    EXTEND = 2
    RETRACT = 4
    STOP1 = 1
    STOP2 = 3
    input = """button input expressed in values 1, 2, and 3"""
    encoderinput = """input from the encoder translated to fit a more simple numeric value"""
    encoderstop1= """quota the encoder must meet to auto-stop the tape measure whilst extended"""
    encoderstop2= """lower limit to the encoder"""

    def __init__(self):
        self.state = Tapemeasure.STOP

    def statecheck(self):
        if self.encoderinput == self.encoderstop1:
            self.input += 1
        elif self.encoderinput == self.encoderstop2:
            self.input +=1
        elif self.input == self.stop1:
            self.stop
        elif self.input == self.stop2:
            self.stop
        elif self.input == self.extend:
            self.extend
        elif self.input ==self.retract:
            self.retract

    def extend(self):
        self.state = Tapemeasure.EXTEND

    def retract(self):
        self.state = Tapemeasure.RETRACT

    def stop(self):
        self.state = Tapemeasure.STOP

    def execute ( self ):
        """Determines action based on input"""
        if self.state == Tapemeasure.STOP:
            self.performStop()
        elif self.state == Tapemeasure.EXTEND:
            self.performExtend()
        elif self.state == Tapemeasure.RETRACT:
            self.performRetract()

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