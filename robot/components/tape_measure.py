import wpilib

class Tapemeasure:

    tape_motor = wpilib.CANTalon
    tape_encoder = """code for CAN talon encoder here"""
    winch_motor = wpilib.CANTalon
    winch_encoder = """code for CAN talon encoder here"""

    TICKS_PER_ROTATION = 300
    FULL_ROTATION_DISTANCE = 3  # in feet

    def __init__(self):
        self.state = 'STOP'
        self.Kp = 0.3
        self.Ki = 0.3
        self.Kd = 0.3

    def getdistance(self):
        ticks = 0  # self.encoder.get()
        return (ticks / Tapemeasure.TICKS_PER_ROTATION) * Tapemeasure.FULL_ROTATION_DISTANCE

    def extend(self):
        '''extends the tapemeasure'''
        if self.getdistance() <= Tapemeasure.encoderstop1:
            self.state = 'EXTEND'
        else:
            self.state = 'STOP'

    def retract(self):
        '''retracts the tapemeasure'''
        if self.getdistance() >= Tapemeasure.esncoderstop2:
            self.state = 'RETRACT'
        else:
            self.state = 'STOP'

    def stop(self):
        '''stops the tapemeasure'''
        self.state = 'STOP'

    def execute ( self ):
        """Determines action based on input"""
        if self.state == 'STOP':
            self.performStop()
        elif self.state == 'EXTEND':
            self.performExtend()
        elif self.state == 'EXTEND':
            self.performRetract()
        else:
            self.state = 'STOP'

    def performExtend (self):
        """activate motors to extend"""
        wpilib.PIDController.enable(self.Kp, self.Ki, self.Kd, self.tape_motor, self.tape_motor )
        wpilib.PIDController.enable(self.Kp, self.Ki, self.Kd, self.winch_motor, self.winch_motor)
    def performRetract (self):
        """activate motors to retract"""
        wpilib.PIDController.enable(self.Kp, self.Ki, self.Kd, self.tape_motor, self.tape_motor)
        wpilib.PIDController.enable(self.Kp, self.Ki, self.Kd, self.winch_motor, self.winch_motor)

    def performStop (self):
        """deactivate motors"""
        wpilib.PIDController.disable(self.Kp, self.Ki, self.Kd, self.tape_motor, self.tape_motor)
        wpilib.PIDController.disable(self.Kp, self.Ki, self.Kd, self.winch_motor, self.winch_motor)