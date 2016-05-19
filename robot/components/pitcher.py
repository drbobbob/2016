
import wpilib 

from magicbot import tunable

class Pitcher: 
   
    pitcher_motor = wpilib.CANTalon
    
    pid_enabled = tunable(True)
    pid_speed = tunable(8000)
    pid_ok = tunable(100)
    
    manual_speed = tunable(1)
    #motor_speed = tunable(0)
    
    manual_ok_time = tunable(1)
    pid_ok_time = tunable(0.5)
    
    MANUAL_MODE = wpilib.CANTalon.ControlMode.PercentVbus
    PID_MODE = wpilib.CANTalon.ControlMode.Speed
    
    def __init__(self):
        self.is_enabled = False
        self.ready_timer = wpilib.Timer()
        self.ready_timer.start()
        self.do_reverse = False
        
    def on_enabled(self):
        # Ensure that the motor isn't ready
        self.ready_timer.reset()
   
    def enable(self):
        """ turn on motor to spin wheel """
        self.is_enabled = True
        self.pid_enabled = True
        
    def disable(self):
        """ turn off motor """
        self.is_enabled = False
        
    def reverse(self):
        self.is_enabled = True
        self.pid_enabled = False
        self.do_reverse = True
        
    def is_ready(self):
       
        if self.pid_enabled:
            return self.ready_timer.get() > self.pid_ok_time
        else:
            return self.ready_timer.get() > self.manual_ok_time
    
    
    def execute(self):
        """ JUST DO IT """
        #if motor is enabled, set motor to 1#
        #if motor is disabled, set motor to 0#
        if self.pid_enabled:
            mode = self.PID_MODE
            speed = self.pid_speed
        
        else:
            mode = self.MANUAL_MODE
            if self.do_reverse:
                speed = -self.manual_speed
            else:
                speed = self.manual_speed
        
        self.pitcher_motor.changeControlMode(mode)
        
        if self.is_enabled:
            self.pitcher_motor.set(speed)
        else:
            self.pitcher_motor.set(0)
            self.ready_timer.reset()
        
        self.is_enabled = False
        self.do_reverse = False
        
        self.motor_speed = self.pitcher_motor.getSpeed()
        
        # Reset timer if not near correct speed
        if self.pid_enabled and abs(self.pid_speed - self.motor_speed) > self.pid_ok:
            self.ready_timer.reset()
        
        