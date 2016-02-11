import wpilib

class Tapemeasure:

    tape_motor = wpilib.CANTalon
    winch_motor = wpilib.CANTalon

    EXTEND = 2
    RETRACT = 4
    STOP = 0
    STOP1 = 1
    STOP2 = 3
    input = """button input expressed in values 1, 2, and 3"""
    encoderinput = """input from the encoder translated to fit a more simple numeric value"""
    encoderstop1= """quota the encoder must meet to auto-stop the tape measure whilst extended"""
    encoderstop2= """lower limit to the encoder"""

    TICKS_PER_ROTATION = 300
    FULL_ROTATION_DISTANCE = 3 # in feet

    def __init__(self):
        self.state = Tapemeasure.STOP

    def getdistance(self):
        ticks = 0 # self.encoder.get()
        return (ticks / Tapemeasure.TICKS_PER_ROTATION) * Tapemeasure.FULL_ROTATION_DISTANCE

    def extend(self):
        if self.getdistance() <= Tapemeasure.encoderstop1:
            self.state = Tapemeasure.EXTEND
        else:
            self.state = Tapemeasure.STOP

    def retract(self):
        if self.getdistance() >= Tapemeasure.esncoderstop2:
            self.state = Tapemeasure.RETRACT
        else:
            self.state = Tapemeasure.STOP

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
        self.state = Tapemeasure.STOP

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