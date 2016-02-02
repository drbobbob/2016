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
        
    def getdistance (self):
        '''sets the distance based on output from distance sensor'''
        
        self.distance = self.Sharp.getDistance()
    
    def ball_in(self):
        '''used to drive the belts so that the boulder goes into the robot'''
        self.beltvelocity = 1
        
    def ball_out(self):
        '''used to drive belts so that the boulder exits the robot'''
        
        self.beltvelocity = -1
        
    def fire(self):
        '''brings ball into shooter which should be at speed before launch'''
        
        self.beltvelocity = 1
            
    def execute(self):
        '''sets final values for belt motors'''
        
        self.beltmotor.set(self.beltvelocity())
        
        
        
        
    