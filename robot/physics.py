#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn 
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#
# NOTE: THIS API IS ALPHA AND WILL MOST LIKELY CHANGE!
#       ... if you have better ideas on how to implement, submit a patch!
#
import math
from pyfrc.physics import drivetrains
from networktables.util import ntproperty

from pyfrc.physics.core import PhysicsInitException
from pyfrc.version import __version__
from distutils.version import LooseVersion

class PhysicsEngine(object):
    '''
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point
    '''
    
    # Transmit data to robot via NetworkTables
    target_present = ntproperty('/components/autoaim/present', False)
    target_angle = ntproperty('/components/autoaim/target_angle', 0)
    target_height = ntproperty('/components/autoaim/target_height', 0)
    
    camera_update_rate = 1/15.0
    
    target_location = (0, 16)
    
    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface` object
                                       to communicate simulation effects to
        '''
        
        if LooseVersion(__version__) < LooseVersion('2016.2.5'):
            raise ValueError("ERROR: must have pyfrc 2016.2.5 or greater installed!")
        
        self.physics_controller = physics_controller
        self.physics_controller.add_device_gyro_channel('navxmxp_spi_4_angle')
        
        self.last_cam_update = -10
            
    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''
        
        # Simulate the drivetrain
        lf_motor = hal_data['CAN'][4]['value']/-1024
        lr_motor = hal_data['CAN'][5]['value']/-1024
        rf_motor = hal_data['CAN'][2]['value']/-1024
        rr_motor = hal_data['CAN'][3]['value']/-1024
        
        speed, rotation = drivetrains.four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor, speed=8)
        self.physics_controller.drive(speed, rotation, tm_diff)
        
        # Simulate the firing mechanism 
         
        
        # Simulate the camera approaching the tower
        # -> this is a very simple approximation, should be good enough
        # -> calculation updated at 15hz
        if now - self.last_cam_update > self.camera_update_rate:
            
            x, y, angle = self.physics_controller.get_position()
            
            tx, ty = self.target_location
            
            dx = tx - x
            dy = ty - y
            
            distance = math.hypot(dx, dy)
            
            target_present = False
            
            if distance > 6 and distance < 17:
                # determine the absolute angle
                target_angle = math.atan2(dy, dx)
                angle = ((angle + math.pi) % (math.pi*2)) - math.pi
                
                # Calculate the offset, if its within 30 degrees then
                # the robot can 'see' it
                offset = math.degrees(target_angle - angle)
                if abs(offset) < 30:
                    target_present = True 
                
                    # target 'height' is a number between -18 and 18, where
                    # the value is related to the distance away. 11 is ideal.
                
                    self.target_angle = offset
                    self.target_height = -(distance*3)+30
                
            self.target_present = target_present
            self.last_cam_update = now

