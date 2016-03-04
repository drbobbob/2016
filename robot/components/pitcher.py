
import wpilib 

from networktables.util import ntproperty

class Pitcher: 
   
    pitcher_motor = wpilib.CANTalon
    
    pid_enabled = ntproperty('/components/pitcher/pid_enabled', True)
    pid_speed = ntproperty('/components/pitcher/pid_speed', 8000)
    pid_ok = ntproperty('/components/pitcher/pid_ok', 100)
    
    manual_speed = ntproperty('/components/pitcher/manual_speed', 1)
    motor_speed = ntproperty('/components/pitcher/motor_speed', 0)
    
    manual_ok_time = ntproperty('/components/pitcher/manual_ok_time', 1)
    pid_ok_time = ntproperty('/components/pitcher/pid_ok_time', 0.5)
    
    MANUAL_MODE = wpilib.CANTalon.ControlMode.PercentVbus
    PID_MODE = wpilib.CANTalon.ControlMode.Speed
    
    def __init__(self):
        self.is_enabled = False
        self.ready_timer = wpilib.Timer()
        self.ready_timer.start()
        
    def on_enabled(self):
        # Ensure that the motor isn't ready
        self.ready_timer.reset()
   
    def enable(self):
        """ turn on motor to spin wheel """
        self.is_enabled = True
        
    def disable(self):
        """ turn off motor """
        self.is_enabled = False
        
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
            speed = self.manual_speed
        
        self.pitcher_motor.changeControlMode(mode)
        
        if self.is_enabled:
            self.pitcher_motor.set(speed)
        else:
            self.pitcher_motor.set(0)
            self.ready_timer.reset()
        
        self.is_enabled = False
        
        self.motor_speed = self.pitcher_motor.getSpeed()
        
        # Reset timer if not near correct speed
        if self.pid_enabled and abs(self.pid_speed - self.motor_speed) > self.pid_ok:
            self.ready_timer.reset()
        
        