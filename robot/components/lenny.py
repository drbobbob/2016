'''
Created on Jan 27, 2016

@author: Miles
'''
import wpilib
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

class Lenny:
    
    beltmotor = wpilib.CANTalon
    sharp = Sharp
    
    '''lenny's matrix self'''
    def __init__(self):
        self.beltvelocity = 0
        self.disabled = False
        
    def ball_detector (self):
        '''I can't tell is it there'''
        self.distance = self.sharp.getDistance()
        
        if self.distance > 5:
            return False
        else:
            return True
    
    def ball_in(self):
        '''come in at your own risk'''
        if self.ball_detector() == False:
            self.beltvelocity = 1
        else:
            self.beltvelocity = 0
        
    def ball_out(self):
        '''geet outa town'''
        if self.ball_detector() == True:
            self.beltvelocity = -1
        else:
            self.beltvelocity = 0
        
    def fire(self):
        '''bye bye boulder. let her rip!'''
        if self.ball_detector() == True:
            self.beltvelocity = 1
        else:
            self.beltvelocity = 0
        
    def stop(self):
        '''stay put. good doggie'''
        self.beltvelocity = 0
        
    def disable(self):
        self.disabled = True
            
    def execute(self):
        '''da "boss".'''
        if self.disabled == False:
            self.beltmotor.set(self.beltvelocity)
        else:
            self.beltmotor.set(0)
            
        self.beltvelocity = 0
        self.disabled = False
        
        
        
    