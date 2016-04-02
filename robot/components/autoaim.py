import hal
import wpilib

from .drive import Drive
from .exposure_control import ExposureControl

from components.pitcher import Pitcher
from components.shooter_control import ShooterControl

from networktables import NetworkTable
from networktables.util import ntproperty

class AutoAim:
    
    LIGHT_ON = wpilib.Relay.Value.kOn
    LIGHT_OFF = wpilib.Relay.Value.kOff
    
    drive = Drive
    pitcher = Pitcher
    shooter_control = ShooterControl
    camera_light = wpilib.Relay 
    
    # Variables from camera
    present = ntproperty('/components/autoaim/present', False)
    #target_angle = ntproperty('/components/autoaim/target_angle', 0)
    
    # Variables to driver station
    camera_enabled = ntproperty('/camera/enabled', False)
    autoaim_enabled = ntproperty('/components/autoaim/enabled', False)
    autoaim_on_target = ntproperty('/components/autoaim/on_target', False)
    target_height = ntproperty('/components/autoaim/target_height', 0)
    height_setpoint = ntproperty('/components/autoaim/height_setpoint', 11)

    if hal.HALIsSimulation():
        kP = 0.2
    else:
        kP = 0.1
        
    kI = 0.00
    kD = 0.00
    kF = 0.00
    
    kToleranceHeight = .3
    
    def __init__(self):
        self.aim_speed = None
        self.aimed_at_angle = None
        
        self.exposure_control = ExposureControl()
        
        # By default, ensure the operator can see through both cameras
        self.exposure_control.set_auto_exposure(device=0)
        self.exposure_control.set_auto_exposure(device=1)
        
        # target angle stuff
        self.target_angle = None
        nt = NetworkTable.getTable('/components/autoaim')
        nt.addTableListener(self._on_update, True, 'target_angle')
        
        self.move_to_target_height_output = None
        distance_controller = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self.get_camera_height, output=self.move_to_target_height)
        distance_controller.setInputRange(-18,  18)
        distance_controller.setOutputRange(-1.0, 1.0)
        distance_controller.setAbsoluteTolerance(self.kToleranceHeight)
        self.distance_controller = distance_controller
        
        
    def get_camera_height(self):
        return self.target_height
    
    def move_to_target_height(self, output):
        self.move_to_target_height_output = output
        
    def is_at_height(self):
        
        return self.distance_controller.isEnable() and self.distance_controller.onTarget()
    
    def _on_update(self, source, key, value, isNew):
        self.target_angle = value
    
    def aim(self, speed=0):
        #stores some value
        self.aim_speed = speed
    
    def execute(self):
        
        autoaim_enabled = self.aim_speed is not None
        
        # Only change camera_enabled on transition, that way the UI can set it
        # True if desired
        if self.autoaim_enabled != autoaim_enabled:
            self.autoaim_enabled = autoaim_enabled
            self.camera_enabled = autoaim_enabled
            
            if autoaim_enabled:
                self.distance_controller.setSetpoint(self.height_setpoint)
                
                # Tracking only works when exposure is turned down
                self.exposure_control.set_dark_exposure(device=0)
            else:
                self.exposure_control.set_auto_exposure(device=0)
                self.distance_controller.disable()
                self.move_to_target_height_output = None
            
        #if autoaim_enabled or self.camera_enabled:
        self.camera_light.set(self.LIGHT_ON)
        #else:
        #self.camera_light.set(self.LIGHT_OFF)
        
        if not autoaim_enabled:
            self.autoaim_on_target = False
            self.aimed_at_angle = None
            return
        
        self.pitcher.enable()
        # work goes here
        if self.present == True:
            current_angle = self.drive.get_angle()
            
            if self.target_angle is not None:
                self.aimed_at_angle = current_angle + self.target_angle
                self.target_angle = None
            
            if self.aimed_at_angle is not None:
                speed = self.move_to_target_height_output
                if speed is None:
                    speed = self.aim_speed
                self.drive.move_at_angle(speed, self.aimed_at_angle)
        
            self.distance_controller.enable()
        else:
            self.distance_controller.disable()
            self.move_to_target_height_output = None
        
        
        self.autoaim_on_target = self.drive.is_at_angle() and self.is_at_height()
        if self.autoaim_on_target == True:
            self.shooter_control.fire()
        
        # reset
        self.aim_speed = None
