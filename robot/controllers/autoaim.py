import hal
import wpilib

from components.drive import Drive
from components.exposure_control import ExposureControl
from components.pitcher import Pitcher

from controllers.angle_controller import AngleController
from controllers.distance_controller import DistanceController
from controllers.position_history import PositionHistory

from .shooter_control import ShooterControl

from magicbot import state, timed_state, StateMachine, tunable
from networktables import NetworkTable
from networktables.util import ntproperty



class AutoAim(StateMachine):
    '''
        Automatically positions the robot so that it can shoot,
        and then shoots.
    '''
    
    LIGHT_ON = wpilib.Relay.Value.kOn
    LIGHT_OFF = wpilib.Relay.Value.kOff
    
    drive = Drive
    pitcher = Pitcher
    shooter_control = ShooterControl
    
    angle_ctrl = AngleController
    distance_ctrl = DistanceController
    
    pos_history = PositionHistory
    
    # Variables to driver station
    camera_enabled = ntproperty('/camera/enabled', False)
    
    autoaim_enabled = tunable(False)
    
    # straight-line approximation for translating pixels to 
    # encoder feet movements
    ideal_height = tunable(-9)
    other_height = tunable(10)
    ideal_encoder = tunable(0)
    other_encoder = tunable(10)
    
    angle_offset = tunable(-10)

    if hal.HALIsSimulation():
        kP = 0.2
    else:
        kP = 0.06
        
    kI = 0.00
    kD = 0.00
    kF = 0.00
    
    kToleranceHeight = 2
    
    def __init__(self):
        self.aimed_at_angle = None
        self.aimed_at_distance = None
        
        self.exposure_control = ExposureControl()
        
        # By default, ensure the operator can see through both cameras
        self.exposure_control.set_auto_exposure(device=0)
        self.exposure_control.set_auto_exposure(device=1)
        
        # target angle stuff
        self.target = None
        
        nt = NetworkTable.getTable('/camera')
        nt.addTableListener(self._on_target, True, 'target')
        
        self.move_to_target_height_output = None
    
    #
    # Internal API
    #
    
    def _on_target(self, source, key, value, isNew):
        self.target = value
        
    def _height_to_distance_offset(self, h):
        '''converts a height to a distance'''
        return ((h - self.other_height) * (self.ideal_encoder - self.other_encoder)) / (self.ideal_height - self.other_height) + self.other_encoder
    
    def _move_to_position(self):
        '''returns true if at correct position, false otherwise'''
        
        # This is the bulk of the logic here.. 
        target = self.target
        
        if target is not None and len(target) > 0:
            
            # copy before using it
            target = target[:]
            
            # old idea: reduce the camera angle by half to compensate for lag
            # new idea: latency compensation
            angle, height, capture_ts = target
            history = self.pos_history.get_position(capture_ts)
            
            if history is not None:
                r_angle, r_position, r_ts = history
                
                #self.aimed_at_angle = self.drive.get_angle_at_ts(capture_ts) + (angle/2.0)
                self.aimed_at_angle = r_angle + angle
                self.aimed_at_distance = r_position + self._height_to_distance_offset(height)
            
            self.target = None
        
        # Tell the robot to go to somewhere
        
        if self.aimed_at_angle is not None:
            self.angle_ctrl.align_to(self.aimed_at_angle)
            
        if self.aimed_at_distance is not None:
            self.distance_ctrl.move_to(self.aimed_at_distance)
        
        return self.is_at_position()
    
    #
    # External API
    #
    
    def aim(self):
        '''Engage the autoaim procedure'''
        self.engage()
    
    def is_at_position(self):
        ''':returns: True when robot is in firing position'''
        return self.distance_ctrl.is_at_location() and \
               self.angle_ctrl.is_aligned()
    
    #
    # State machine
    #
    
    @state(first=True)
    def initial_state(self):
        
        # Ensure that stale data is removed
        self.target = None
        self.aimed_at_angle = None
        self.aimed_at_distance = None
        
        self.pos_history.enable()
        
        # Tracking only works when exposure is turned down
        self.exposure_control.set_dark_exposure(device=0)
        self.camera_enabled = True
        
        self.next_state_now('moving_to_position')
            
    @state
    def moving_to_position(self):
        '''Cause the robot to automatically move to the correct position to shoot'''
        
        # Don't care about whether the image is 'present', the target
        # angle/height will be set when it is, and if there's a blip where the
        # camera can't see the target we don't want to interrupt the operators
        # movements
        
        if self._move_to_position():
            # at the right place? ok, transition!
            self.next_state('at_position')
    
    @timed_state(duration=0.75, next_state='begin_firing')
    def at_position(self):
        '''Only go to 'begin_firing' if we've been at the right position for
        more than a set period of time'''
        
        if not self._move_to_position():
            # if we're no longer on the right spot, reset
            self.next_state('moving_to_position')
    
    @state
    def begin_firing(self):
        '''At the correct position, fire the ball'''
        
        # TODO: should move to position still? Now that vibration
        #       is less of an issue, could continuously adjust?
        # if not self._move_to_position():
        #     self.next_state_now('moving_to_position')
        # else: .. 
        
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
        
        self.pos_history.disable()
        
        self.camera_enabled = False
        self.on_target = False
        self.exposure_control.set_auto_exposure(device=0)
