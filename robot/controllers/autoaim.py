import hal
import wpilib

import math
import threading

from components.drive import Drive
from components.exposure_control import ExposureControl

from components.pitcher import Pitcher

from .shooter_control import ShooterControl

from magicbot import state, timed_state, StateMachine, tunable
from networktables import NetworkTable
from networktables.util import ntproperty

class AutoAim(StateMachine):
    
    LIGHT_ON = wpilib.Relay.Value.kOn
    LIGHT_OFF = wpilib.Relay.Value.kOff
    
    drive = Drive
    pitcher = Pitcher
    shooter_control = ShooterControl
    
    # Variables from camera
    #target_angle = ntproperty('/components/autoaim/target_angle', 0)
    
    # Variables to driver station
    camera_enabled = ntproperty('/camera/enabled', False)
    
    present = tunable(False)
    autoaim_enabled = tunable(False)
    height_setpoint = tunable(-9)
    
    height_decay = tunable(0.2)
    decayed_height = tunable(0)

    if hal.HALIsSimulation():
        kP = 0.2
    else:
        kP = 0.06
        
    kI = 0.00
    kD = 0.00
    kF = 0.00
    
    kToleranceHeight = 2
    
    def __init__(self):
        self.aim_speed = None
        self.aimed_at_angle = None
        
        self.exposure_control = ExposureControl()
        
        # By default, ensure the operator can see through both cameras
        self.exposure_control.set_auto_exposure(device=0)
        self.exposure_control.set_auto_exposure(device=1)
        
        # target angle stuff
        self.target_angle = None
        self.target_height = None
        self.target_height_lock = threading.Lock()
        
        nt = NetworkTable.getTable('/components/autoaim')
        nt.addTableListener(self._on_target_angle, True, 'target_angle')
        nt.addTableListener(self._on_target_height, True, 'target_height')
        
        self.move_to_target_height_output = None
        distance_controller = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self._pidGet, output=self._pidWrite)
        distance_controller.setInputRange(-18,  18)
        distance_controller.setOutputRange(-1.0, 1.0)
        distance_controller.setAbsoluteTolerance(self.kToleranceHeight)
        self.distance_controller = distance_controller
        
        distance_controller.initTable(nt.getSubTable('pid'))
    
    #
    # Internal API
    #
    
    def _pidGet(self):
        if self.target_height is None:
            return self.height_setpoint # until we get something
        else:
            with self.target_height_lock:
                # decay the value: avoid race conditions
                decay = (self.height_setpoint - self.target_height)*self.height_decay
                self.target_height += decay
            
            # debug usage
            self.decayed_height = self.target_height
            return self.target_height
    
    def _pidWrite(self, output):
        
        
        if self.target_height is None:
            self.move_to_target_height_output = 0
        else:
            # y: 0.15 to 0.6
            output = -output
            self.move_to_target_height_output = math.copysign(abs(output)*0.45+0.15, output)
        
    def _on_target_angle(self, source, key, value, isNew):
        self.target_angle = value
        
    def _on_target_height(self, source, key, value, isNew):
        with self.target_height_lock:
            self.target_height = value
        
    #
    # External API
    #
    
    def is_at_height(self):
        return self.target_height is not None and self.distance_controller.onTarget()
    
    def aim(self, speed=0):
        #stores some value
        self.aim_speed = speed
        self.engage()
    
    @state(first=True)
    def initial_state(self):
        
        # Initially set these to None, they will be updated when a real input
        # value comes in
        self.target_angle = None
        self.target_height = None
        
        # Tracking only works when exposure is turned down
        self.exposure_control.set_dark_exposure(device=0)
        self.distance_controller.setSetpoint(self.height_setpoint)
        self.distance_controller.enable()
        self.camera_enabled = True
        
        self.next_state_now('moving_to_position')
            
    @state
    def moving_to_position(self):
        '''Cause the robot to automatically move to the correct position to shoot'''
        
        # Don't care about whether the image is 'present', the target
        # angle/height will be set when it is, and if there's a blip where the
        # camera can't see the target we don't want to interrupt our movement
        
        if self._move_to_position():
            # at the right place? ok, transition!
            self.next_state('at_position')
        
        #if self.present:
        #else:
        #    self.distance_controller.disable()
    
    @timed_state(duration=0.5, next_state='begin_firing')
    def at_position(self):
        '''Only go to 'begin_firing' if we've been at the right position for
        more than a set period of time'''
        
        if not self._move_to_position() and self.present:
            # if we're no longer on the right spot, reset
            self.next_state('moving_to_position')
    
    def _move_to_position(self):
        '''returns true if at correct position, false otherwise'''
        
        if self.target_angle is not None:
            # reduce the camera angle by half to compensate for lag
            self.aimed_at_angle = self.drive.get_angle() + (self.target_angle/2.0)
            self.target_angle = None
            
        at_height = self.is_at_height()
        
        if self.aimed_at_angle is not None:
            if at_height:
                # No moving required if already there.. 
                speed = 0
            else:
                speed = self.move_to_target_height_output
                if speed is None:
                    speed = self.aim_speed
            
            self.drive.move_at_angle(speed, self.aimed_at_angle)
    
        on_target = self.drive.is_at_angle() and at_height
        self.on_target = on_target
        return on_target
    
    @state
    def begin_firing(self):
        '''At the correct position, fire the ball'''
        self.drive.move(0, 0)
        self.shooter_control.fire()
        
        # Wait for the shooter to report that it has fired
        if self.shooter_control.is_firing():
            self.next_state_now('firing')
    
    @timed_state(duration=0.5, must_finish=True, next_state='end')
    def firing(self):
        '''Waits for the ball to exit before allowing the operator to move'''
        self.drive.move(0, 0)
    
    @state
    def end(self):
        '''Just sit until the operator lets go of the joystick'''
        pass
    
    def done(self):
        super().done()
        
        self.camera_enabled = False
        self.on_target = False
        self.exposure_control.set_auto_exposure(device=0)
        self.distance_controller.disable()