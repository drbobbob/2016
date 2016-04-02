
import os
from os.path import exists
import shutil
import threading

import hal
import wpilib

import logging
logger = logging.getLogger('exposure_control')

from networktables import NetworkTable

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
    dark_args = '-c exposure_auto=1 -c exposure_absolute=10' # tried 10, was too bright.. 
    
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
        
        self.nt = NetworkTable.getTable('/camera/exposure')
        self.nt.addTableListener(self._on_nt_change, False)
        
        wpilib.Resource._add_global_resource(self)
    
    def free(self):
        '''Cleans up the thread'''
        if self.enabled:
            with self.lock:
                self.enabled = False
                self.lock.notify()
                
            self.thread.join()
            
    def _on_nt_change(self, s, k, v, n):
        try:
            device = int(k)
        except ValueError:
            pass
        else:
            self._set_exposure(device, v)
    
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
                
                vv = getattr(self, '%s_args' % v, None)
                
                if vv is None:
                    logger.warn("Device %s: Invalid exposure setting %s", k, v)
                else:
                    logger.info("Device %s: %s", k, vv)
                    if self._v4l_path:
                        
                        fname = '/dev/video%d' % k
                        if exists(fname):
                            os.system('%s -d %s %s' % (self._v4l_path, k, vv))
                        else:
                            logger.warn("Camera not found at %s", fname)
                    
                settings[k] = v
                self.nt.putString(str(k), v)
    
    def _set_exposure(self, device, typ):
        with self.lock:
            self.settings[device] = typ
            self.lock.notify()     
    
    def set_auto_exposure(self, device=0):
        '''Tells a camera to go into auto exposure mode'''
        self._set_exposure(device, 'auto')
    
    def set_dark_exposure(self, device=0):
        '''Tells a camera to go into dark exposure mode'''
        self._set_exposure(device, 'dark')

        