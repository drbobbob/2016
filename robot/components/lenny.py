'''
Created on Jan 27, 2016

@author: Miles
'''
import wpilib
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

class Lenny():
    
    x = 0
    
    def ball_in(self):
        '''used to drive the belts so that the boulder goes into the robot'''
        x = 1
        
    def ball_out(self):
        '''used to drive belts so that the boulder exits the robot'''
        
        x = -1
        
    def fire(self):
        '''brings ball into shooter which should be at speed before launch'''
        
        x = 1
            
    def execute(self):
        
        self.belt = wpilib.CANTalon(1)
        
        if Sharp.getDistance(self) > 14:
            self.belt.set(x)
        else:
            self.belt.set(0)
        
    
    
    