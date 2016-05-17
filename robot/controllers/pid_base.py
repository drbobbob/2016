
import threading

import wpilib
from networktables import NetworkTable

class BasePIDComponent:
    '''
        Base for a component that has a PIDController controlling its output.
        
        readonly variables for subclasses:
        
        * self.enabled: set to True if enabled (only read this)
        * self.rate: set to the calculated rate if enabled, None otherwise
        
        variables that subclasses should set:
        
        * self.setpoint: must be set each period to enable the controller
        
        # TODO: add a 'settle time' output variable
    '''
    
    def __init__(self, pid_input, table_name):
        
        self.enabled = False
        self.rate = None
        self.setpoint = None
        
        # protects enabled/rotation_rate
        self.lock = threading.RLock()
        
        self.pid = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, pid_input, output=self)
        
        # TODO: magicbot should initialize this for us..
        self.pid.initTable(NetworkTable.getTable('/components/%s/pid' % table_name))
      
    def pidWrite(self, output):
        # prevent race condition (https://github.com/wpilibsuite/allwpilib/issues/30)
        with self.lock:
            if self.enabled:
                self.rate = output
    
    def execute(self):
        
        # set the initial setpoint before enabling the PIDController!
        if self.setpoint is not None:
            self.pid.setSetpoint(self.setpoint)

            # if self.enabled was not previously set, enable the controller
            # -> no lock required, not messing with rate
            if not self.enabled:
                self.pid.enable()
                self.enabled = True
        
        else:
            # prevent race condition when interacting with enabled/rotation_rate 
            with self.lock:
                if self.enabled:
                    self.pid.disable()
                    self.enabled = False
                    self.rate = None
        
        self.setpoint = None

