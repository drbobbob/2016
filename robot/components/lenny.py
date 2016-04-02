'''
Created on Jan 27, 2016

@author: Miles
'''
import wpilib
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

from networktables.util import ntproperty

class Lenny:
    
    beltmotor = wpilib.CANTalon
    ball_sensor = Sharp
    
    ball_detected = ntproperty('/components/lenny/ball_detected', False)
    ball_detected_distance = ntproperty('/components/lenny/ball_detected_distance', 0)
    ball_detected_threshold = ntproperty('/components/lenny/ball_detected_threshold', 11.5)
    beltvelocity_in = ntproperty('/components/lenny/beltvelocity_in', -1)
    beltvelocity_out = ntproperty('/components/lenny/beltvelocity_out', 1)

   # start of extra variables#
    pid_enabled = ntproperty('/components/lenny/pid_enabled', True)
    pid_speed = ntproperty('/components/lenny/pid_speed', 8000)
    manual_speed = ntproperty('/components/lenny/manual_speed', 1)
    motor_speed = ntproperty('/components/lenny/motor_speed', 0)
    manual_ok_time = ntproperty('/components/lenny/manual_ok_time', 1)
    pid_ok_time = ntproperty('/components/lenny/pid_ok_time', 0.5)

    MANUAL_MODE = wpilib.CANTalon.ControlMode.PercentVbus
    PID_MODE = wpilib.CANTalon.ControlMode.Speed

    #lenny's matrix self
    def __init__(self):
        self.beltvelocity = 0
        self.disabled = False
        self.is_enabled = False
        self.ready_timer = wpilib.Timer()
        self.ready_timer.start()
        self.pid_enabled = False
        
    def is_ball_detected(self):
        #I can't tell is it there
        self.ball_detected_distance = self.ball_sensor.getDistance()
        self.ball_detected = self.ball_detected_distance < self.ball_detected_threshold
        return self.ball_detected
    
    def ball_in(self, force=False, pid=False):
        #come in at your own risk
        if force != False:
            self.beltvelocity = force
        elif not self.is_ball_detected():
            self.beltvelocity = self.beltvelocity_in
        else:
            self.beltvelocity = 0

        self.pid_enabled = pid
        
    def ball_out(self):
        #geet outa town
        self.beltvelocity = self.beltvelocity_out
        
    def disable(self):
        self.disabled = True
            
    def execute(self):
        #da "boss"
        self.is_ball_detected()
        
        if self.disabled == False:
            mode = self.PID_MODE if self.pid_enabled else self.MANUAL_MODE
            self.beltmotor.changeControlMode(mode)
            self.beltmotor.set(self.beltvelocity)
        else:
            self.beltmotor.set(0)

        self.beltvelocity = 0
        self.disabled = False
        self.pid_enabled = False
