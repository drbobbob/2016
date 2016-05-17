
import wpilib
import hal
from networktables import NetworkTable
from magicbot import tunable
from components.lenny import Lenny
from .pid_base import BasePIDComponent


class AutoLenny(BasePIDComponent):

	if hal.HALIsSimulation():
		kP = 0.1
		kI = 0
		kD = 0
		kF = 0
	else:
		kP = 0.1
		kI = 0
		kD = 0
		kF = 0

	kTolerance = 2

	lenny = Lenny
	
	def __init__(self):


		super().__init__(self.get_lenny, 'auto_lenny')

		self.pid.setInputRange(0,  40)
		self.pid.setOutputRange(-1.0, 1.0)
		self.pid.setAbsoluteTolerance(self.kTolerance)

	def enable(self):
		
		self.setpoint = self.lenny.loader_position

	def get_lenny(self):
		return self.lenny.get_distance()



	def execute(self):
		
		super().execute()

		if self.rate is not None:
			self.lenny.set(self.rate if self.lenny.is_ball_detected() else 0)

