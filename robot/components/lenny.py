'''
Created on Jan 27, 2016

@author: Miles
'''
import wpilib
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

class Lenny():

    def __init__(self):
        self.beltvelocity = 0
        self.beltmotor = wpilib.CANTalon(0)
        self.Sharp = Sharp(0)
        
    def ball_detector (self):
        '''I can't tell is it there'''
        
        self.distance = self.Sharp.getDistance()
        
        if self.distance > 5:
            return False
        
        else:
            return True
    
    def ball_in(self):
        '''come in at your own risk'''
        self.beltvelocity = 1
        
    def ball_out(self):
        '''geet outa town'''
        
        self.beltvelocity = -1
        
    def fire(self):
        '''bye bye boulder. let her rip!'''
        
        self.beltvelocity = 1
        
    def disable(self):
        '''stay put. good doggie'''
        
        self.beltvelocity = 0
            
    def execute(self):
        '''the "boss".'''
        
        self.beltmotor.set(self.beltvelocity())
        
        
        
        
    