
import wpilib

from .drive import Drive

from networktables import NetworkTable
from networktables.util import ntproperty

class AutoAim:
    
    drive = Drive
    
    present = ntproperty('/components/autoaim/present', False)
    #target_angle = ntproperty('/components/autoaim/target_angle', 0)
    
    
    def __init__(self):
        self.aim_speed = None
        self.aimed_at_angle = None
        
        # target angle stuff
        self.target_angle = None
        nt = NetworkTable.getTable('/components/autoaim')
        nt.addTableListener(self._on_update, True, 'target_angle')
    
    def _on_update(self, source, key, value, isNew):
        self.target_angle = value
    
    def aim(self, speed=0):
        #stores some value
        self.aim_speed = speed
    
    def execute(self):
        
        if self.aim_speed is None:
            self.aimed_at_angle = None
            return
        
        # work goes here
        if self.present == True:
            current_angle = self.drive.get_angle()
            
            if self.target_angle is not None:
                print("Changed to", current_angle, self.target_angle)
                self.aimed_at_angle = current_angle + self.target_angle
                self.target_angle = None
            
            if self.aimed_at_angle is not None:
                print("Going to", current_angle, self.aimed_at_angle)
                self.drive.move_at_angle(self.aim_speed, self.aimed_at_angle)
        
        # reset
        self.aim_speed = None
