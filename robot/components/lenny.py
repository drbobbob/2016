'''
Created on Jan 27, 2016

@author: Miles
'''
import wpilib

class Lenny():
    
    def ball_in(self):
        pass
    
    def ball_out(self):
        pass
    
class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):
        pass
    def teleopPeriodic(self):
        pass
    def teleopInit(self):
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)
    
    