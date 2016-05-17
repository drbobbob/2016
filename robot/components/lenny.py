'''
Created on Jan 27, 2016

@author: Miles
'''
import wpilib
from robotpy_ext.common_drivers.distance_sensors import SharpIRGP2Y0A41SK0F as Sharp

from magicbot import tunable

class Lenny:
    
    beltmotor = wpilib.CANTalon
    ball_sensor = Sharp
    
    loader_position = tunable(12)
    ball_detected_distance = tunable(0)
    ball_detected_threshold = tunable(35)
    ball_detected = tunable(False)
    belt_velocity = tunable(0)
    
    motor_setpoint_in = tunable(-1)
    motor_setpoint_out = tunable(1)
    motor_setpoint_shoot = tunable(-700)
    
    MANUAL_MODE = wpilib.CANTalon.ControlMode.PercentVbus
    PID_MODE = wpilib.CANTalon.ControlMode.Speed

    #lenny's matrix self
    def __init__(self):
        self.motor_setpoint = 0
        self.disabled = False
        self.is_enabled = False
        self.ready_timer = wpilib.Timer()
        self.ready_timer.start()
        self.pid_enabled = False
        
    def is_ball_detected(self):
        #I can't tell is it there
        return self.ball_sensor.getDistance() < self.ball_detected_threshold

    def get_distance_from_loader(self):
          return self.ball_sensor.getDistance() - self.loader_position
 
    def get_distance(self):
        return self.ball_sensor.getDistance()

    def set(self, speed):
          '''Sets lenny to a particular speed'''
          self.motor_setpoint = speed
    
    def ball_in(self):
        '''Brings the ball in if a ball is not detected'''
        if not self.get_distance_from_loader() < self.loader_position:
            self.motor_setpoint = self.motor_setpoint_in
        
    def ball_out(self):
        '''Expels the ball'''
        self.motor_setpoint = self.motor_setpoint_out
        
    def ball_shoot(self):
        '''Sets a speed to shoot the ball out'''
        self.motor_setpoint = self.motor_setpoint_shoot
        self.pid_enabled = True
        
    def disable(self):
        self.disabled = True
            
    def execute(self):
        #da "boss"

        self.ball_detected_distance = self.ball_sensor.getDistance()
        self.ball_detected = self.is_ball_detected()
        self.belt_velocity = self.beltmotor.getEncVelocity()
        
        if self.disabled == False:
            mode = self.PID_MODE if self.pid_enabled else self.MANUAL_MODE
            self.beltmotor.changeControlMode(mode)
            self.beltmotor.set(self.motor_setpoint)
        else:
            self.beltmotor.set(0)

        self.motor_setpoint = 0
        self.disabled = False
        self.pid_enabled = False
