
import os
import shutil
import threading

import hal
import wpilib

import logging
logger = logging.getLogger('exposure_control')

class CommandNotFound(Exception):
    pass

class ExposureControl:
    '''
        Controls the exposure of cameras connected to the robot. Two
        states are defined for now: auto and dark
        
        Requires v4l-utils to be installed
    '''
    
    # These are settings that work for the LifeCam HD-3000
    auto_args = '-c exposure_auto=3'
    dark_args = '-c exposure_auto=1 -c exposure_absolute=10'
    
    def __init__(self):
        
        if not hal.HALIsSimulation():
            self._v4l_path = shutil.which('v4l2-ctl')
            if not self._v4l_path:
                raise CommandNotFound('v4l2-ctl could not be found, did you install v4l-utils?')
        else:
            self._v4l_path = None
        
        self.settings = {}
        self.enabled = True
        
        self.lock = threading.Condition()
        self.thread = threading.Thread(target=self._thread, daemon=True)
        self.thread.start()
        
        wpilib.Resource._add_global_resource(self)
    
    def free(self):
        '''Cleans up the thread'''
        if self.enabled:
            with self.lock:
                self.enabled = False
                self.lock.notify()
                
            self.thread.join()
    
    def _thread(self):
        
        settings = {}
        
        while True:
            with self.lock:
                while self.enabled and self.settings == settings:
                    self.lock.wait()
                    
                if not self.enabled:
                    break
                    
                to_set = self.settings.copy()
                    
            # change settings outside of the lock
            for k, v in to_set.items():
                # Only change when necessary
                if v == settings.get(k):
                    continue
                
                logger.info("Device %s: %s", k, v)
                if self._v4l_path:
                    os.system('%s -d %s %s' % (self._v4l_path, k, v))
                    
                settings[k] = v
    
    def _set_exposure(self, device, args):
        with self.lock:
            self.settings[device] = args
            self.lock.notify()     
    
    def set_auto_exposure(self, device=0):
        '''Tells a camera to go into auto exposure mode'''
        self._set_exposure(device, self.auto_args)
    
    def set_dark_exposure(self, device=0):
        '''Tells a camera to go into dark exposure mode'''
        self._set_exposure(device, self.dark_args)

        