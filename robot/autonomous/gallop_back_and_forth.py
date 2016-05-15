from magicbot import timed_state, AutonomousStateMachine

from components.drive import Drive

class GallopBackAndForth(AutonomousStateMachine):

	MODE_NAME = 'Gallop Back and Forth'


	drive = Drive

	def initialize(self):
		pass
    
	def on_enable(self):
		AutonomousStateMachine.on_enable(self)
		self.drive.reset_angle()

	@timed_state(duration=1.7, next_state="drive_backward", first=True)
	def drive_forward(self):
		self.drive.move_at_angle(1, 0)
		
	@timed_state(duration=1.7)
	def drive_backward(self):
		self.drive.move_at_angle(-1,0)