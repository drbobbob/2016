
import wpilib

from .drive import Drive

from networktables import NetworkTable
from networktables.util import ntproperty

class AutoAim:
    
    drive = Drive
    
    # Variables from camera
    present = ntproperty('/components/autoaim/present', False)
    #target_angle = ntproperty('/components/autoaim/target_angle', 0)
    
    # Variables to driver station
    autoaim_enabled = ntproperty('/components/autoaim/enabled', False)
    autoaim_on_target = ntproperty('/components/autoaim/on_target', False)
    
    
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
        
        autoaim_enabled = self.aim_speed is not None
        
        if self.autoaim_enabled != autoaim_enabled:
            self.autoaim_enabled = autoaim_enabled
        
        if not autoaim_enabled:
            self.autoaim_on_target = False
            self.aimed_at_angle = None
            return
        
        # work goes here
        if self.present == True:
            current_angle = self.drive.get_angle()
            
            if self.target_angle is not None:
                self.aimed_at_angle = current_angle + self.target_angle
                self.target_angle = None
            
            if self.aimed_at_angle is not None:
                self.drive.move_at_angle(self.aim_speed, self.aimed_at_angle)
        
        self.autoaim_on_target = self.drive.is_at_angle()
        
        # reset
        self.aim_speed = None
