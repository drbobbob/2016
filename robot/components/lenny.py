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
    
    ball_detected = ntproperty('/components/lenny/ball_detected', True)
    ball_detected_distance = ntproperty('/components/lenny/ball_detected_distance', 0)
    ball_detected_threshold = ntproperty('/components/lenny/ball_detected_threshold', 8)
    beltvelocity_in = ntproperty('/components/lenny/beltvelocity_in', -1)
    beltvelocity_out = ntproperty('/components/lenny/beltvelocity_out', 1)
    
    '''lenny's matrix self'''
    def __init__(self):
        self.beltvelocity = 0
        self.disabled = False
        
    def is_ball_detected(self):
        '''I can't tell is it there'''
        self.ball_detected_distance = self.ball_sensor.getDistance()
        self.ball_detected = self.ball_detected_distance < self.ball_detected_threshold
        return self.ball_detected
    
    def ball_in(self, force=False):
        '''come in at your own risk'''
        if force != False:
            self.beltvelocity = force
        elif not self.is_ball_detected():
            self.beltvelocity = self.beltvelocity_in
        else:
            self.beltvelocity = 0
        
    def ball_out(self):
        '''geet outa town'''
        self.beltvelocity = self.beltvelocity_out
        
    def disable(self):
        self.disabled = True
            
    def execute(self):
        '''da "boss".'''
        self.is_ball_detected()
        
        if self.disabled == False:
            self.beltmotor.set(self.beltvelocity)
        else:
            self.beltmotor.set(0)
            
        self.beltvelocity = 0
        self.disabled = False
        
        
        
    