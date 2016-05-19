'''
    Copyright (C) 2012-2016 Dustin Spicuzza
    Copyright (C) 2016 Stanislav Ponomarev

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


    Can run this on the roborio by executing mjpg-streamer like so:

    mjpg_streamer -i 'input_opencv.so -r 320x240 --fps 5 --quality 10 --filter /usr/local/lib/mjpg-streamer/cvfilter_py.so --fargs /home/admin/TargetFinder.py'

    Note that because mjpg-streamer is re-encoding the images, by
    setting the quality lower you significantly reduce the CPU usage.
    
    We've seen the following results:
    
    * Quality 30: ~30% CPU at rest
    * Quality 10: ~10% CPU at rest
    
'''

import cv2
import math
import numpy as np
import os
import os.path
import shutil
import sys
import threading
import time

from networktables import NetworkTable, NumberArray
from networktables.util import ntproperty


class Storage:
    
    location_root = '/media/sda1/camera'
    
    logging_error = ntproperty('/camera/logging_error', False, writeDefault=True)
    capture_period = ntproperty('/camera/capture_period', 0.5)
    
    def __init__(self):
        self._location = None
        self.has_image = False
        self.size = None
        self.lock = threading.Condition()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def set_image(self, img):
        
        if self.logging_error:
            return
        
        if self.size is None or self.size[0] != img.shape[0] or self.size[1] != img.shape[1]:
            h, w = img.shape[:2]
            self.size = (h, w)
            
            self.out1 = np.empty((h, w, 3), dtype=np.uint8)
            self.out2 = np.empty((h, w, 3), dtype=np.uint8)
        
        with self.lock:
            cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0,0,255), dst=self.out1)
            self.has_image = True
            self.lock.notify()
    
    @property
    def location(self):
        if self._location is None:
            
            # This assures that we only log when a USB memory stick is plugged in
            if not os.path.exists(self.location_root):
                raise IOError("Logging disabled, %s does not exist" % self.location_root)
            
            # Can't do this when program starts, time might be wrong. Ideally by now the DS
            # has connected, so the time will be correct
            self._location = self.location_root + '/%s' % time.strftime('%Y-%m-%d %H.%M.%S')
            print("Logging to", self._location)
            os.makedirs(self._location, exist_ok=True)
            
        return self._location
    
    def _run(self):
        
        last = time.time()
        
        print("Thread started")
        
        self.logging_error = False
        
        try:
        
            while True:
                with self.lock:
                    now = time.time()
                    while (not self.has_image) or (now - last) < self.capture_period:
                        self.lock.wait()
                        now = time.time()
                        
                    self.out2, self.out1 = self.out1, self.out2
                    self.has_image = False
                
                
                fname = '%s/%.2f.jpg' % (self.location, now)
                cv2.imwrite(fname, self.out2)
                
                last = now
                
        except IOError as e:
            print("Error logging images", e)
        finally:
            self.logging_error = True
            
        print("Thread exited")
    
class TargetFinder:
    
    # Values for the lifecam-3000
    #VFOV = 34.3 # Camera's vertical field of view
    VFOV = 45.6
    HFOV = 61 # Camera's horizontal field of view
    
    VFOV_2 = VFOV / 2.0
    HFOV_2 = HFOV / 2.0
    
    target_center = 7.66 # 7' 8in
    
    camera_height = 1.08 # 13in
    camera_pitch = 40.0
    
    tcx = target_center - camera_height
    
    
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)
    BLUE = (255, 0, 0)
    MOO = (255, 255, 0)
    
    colorspace = cv2.COLOR_BGR2HSV
    
    enabled = ntproperty('/camera/enabled', False)
    logging_enabled = ntproperty('/camera/logging_enabled', False, writeDefault=True)
    
    min_width = ntproperty('/camera/min_width', 20)
    #intensity_threshold = ntproperty('/camera/intensity_threshold', 75)
    
    #target_present = ntproperty('/components/autoaim/present', False)
    #target_angle = ntproperty('/components/autoaim/target_angle', 0)
    #target_height = ntproperty('/components/autoaim/target_height', 0)

    # boston 2013: 30 75 188 255 16 255
    # virginia 2014: ?
    # test image:  43 100 0 255 57 255

    thresh_hue_p = ntproperty('/camera/thresholds/hue_p', 0)
    thresh_hue_n = ntproperty('/camera/thresholds/hue_n', 255)
    thresh_sat_p = ntproperty('/camera/thresholds/sat_p', 145)
    thresh_sat_n = ntproperty('/camera/thresholds/sat_n', 255)
    thresh_val_p = ntproperty('/camera/thresholds/val_p', 80)
    thresh_val_n = ntproperty('/camera/thresholds/val_n', 255)
    
    draw = ntproperty('/camera/draw_targets', True)
    draw_thresh = ntproperty('/camera/draw_thresh', False)
    draw_c1 = ntproperty('/camera/draw_c1', False)
    draw_c2 = ntproperty('/camera/draw_c2', False)
    draw_other = ntproperty('/camera/draw_other', False)
    draw_hue = ntproperty('/camera/draw_hue', False)
    draw_sat = ntproperty('/camera/draw_sat', False)
    draw_val = ntproperty('/camera/draw_val', False)
    
    def __init__(self):
        self.size = None
        self.storage = Storage()
        self.nt = NetworkTable.getTable('/camera')
        
        self.target = NumberArray()
        self.nt.putValue('target', self.target)
        
        # TODO: this makes this no longer tunable.. 
        self.lower = np.array([self.thresh_hue_p, self.thresh_sat_p, self.thresh_val_p], dtype=np.uint8)
        self.upper = np.array([self.thresh_hue_n, self.thresh_sat_n, self.thresh_val_n], dtype=np.uint8)
    
    def preallocate(self, img):
        if self.size is None or self.size[0] != img.shape[0] or self.size[1] != img.shape[1]:
            h, w = img.shape[:2]
            self.size = (h, w)
            
            # these are preallocated so we aren't allocating all the time
            self.gray = np.empty((h, w, 1), dtype=np.uint8)
            self.thresh = np.empty((h, w, 1), dtype=np.uint8)
            self.out = np.empty((h, w, 3), dtype=np.uint8)
            
            self.bin = np.empty((h, w, 1), dtype=np.uint8)
            self.hsv = np.empty((h, w, 3), dtype=np.uint8)
            self.hue = np.empty((h, w, 1), dtype=np.uint8)
            self.sat = np.empty((h, w, 1), dtype=np.uint8)
            self.val = np.empty((h, w, 1), dtype=np.uint8)
            
            # for overlays
            self.zeros = np.zeros((h, w, 1), dtype=np.bool)
            self.black = np.zeros((h, w, 3), dtype=np.uint8)
            
            if True:
                k = 2
                offset = (0,0)
                self.kHoleClosingIterations = 1 # originally 9
                
                self.kMinWidth = 2
                
                # drawing 
                self.kThickness = 1
                self.kTgtThickness = 1 
                
                # accuracy of polygon approximation
                self.kPolyAccuracy = 10.0
                
                self.morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k,k), anchor=offset)
            
        # Copy input image to output
        cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=self.RED, dst=self.out)

    def threshold(self, img):
        
        cv2.cvtColor(img, self.colorspace, dst=self.hsv)
        
        
        cv2.inRange(self.hsv, self.lower, self.upper, dst=self.bin)
        
        if False:
            cv2.split(self.hsv, [self.hue, self.sat, self.val])
            
            # Threshold each component separately
            
            # Hue
            cv2.threshold(self.hue, self.thresh_hue_p, 255, type=cv2.THRESH_BINARY, dst=self.bin)
            cv2.threshold(self.hue, self.thresh_hue_n, 255, type=cv2.THRESH_BINARY_INV, dst=self.hue)
            cv2.bitwise_and(self.hue, self.bin, self.hue)
            
            if self.draw_hue:
            #    # overlay green where the hue threshold is non-zero
                self.out[np.dstack((self.zeros, self.hue != 0, self.zeros))] = 255
            
            # Saturation
            cv2.threshold(self.sat, self.thresh_sat_p, 255, type=cv2.THRESH_BINARY, dst=self.bin)
            cv2.threshold(self.sat, self.thresh_sat_n, 255, type=cv2.THRESH_BINARY_INV, dst=self.sat)
            cv2.bitwise_and(self.sat, self.bin, self.sat)
            
            if self.draw_sat:
                # overlay blue where the sat threshold is non-zero
                self.out[np.dstack((self.sat != 0, self.zeros, self.zeros))] = 255
            
            # Value
            cv2.threshold(self.val, self.thresh_val_p, 255, type=cv2.THRESH_BINARY, dst=self.bin)
            cv2.threshold(self.val, self.thresh_val_n, 255, type=cv2.THRESH_BINARY_INV, dst=self.val)
            cv2.bitwise_and(self.val, self.bin, self.val)
            
            if self.draw_val:
                # overlay red where the val threshold is non-zero
                self.out[np.dstack((self.zeros, self.zeros, self.val != 0))] = 255
            
            # Combine the results to obtain our binary image which should for the most
            # part only contain pixels that we care about        
            cv2.bitwise_and(self.hue, self.sat, self.bin)
            cv2.bitwise_and(self.bin, self.val, self.bin)

        # Fill in any gaps using binary morphology
        cv2.morphologyEx(self.bin, cv2.MORPH_CLOSE, self.morphKernel, dst=self.bin, iterations=self.kHoleClosingIterations)
    
        if self.draw_thresh:
            b = (self.bin != 0)
            cv2.copyMakeBorder(self.black, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=self.RED, dst=self.out)
            self.out[np.dstack((b, b, b))] = 255
        
        #
        return self.bin
    
    #def threshold
    #    cv2.cvtColor(img,cv2.COLOR_BGR2GRAY, dst=self.gray)
    #    ret, _ = cv2.threshold(self.gray, self.intensity_threshold, 255, cv2.THRESH_BINARY, dst=self.thresh)
        

    def find_contours(self, img):
        
        thresh_img = self.threshold(img)
        
        _, contours, _ = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        result = []
        
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            #print(i, len(approx))
            if len(approx)>5 and len(approx)<12:
                _,_,w,h = cv2.boundingRect(approx)
                
                if self.draw_c1:
                    cv2.drawContours(self.out, [approx], -1, self.MOO, 2, lineType=8)
        
                if w > h and w > self.min_width:      
                    result.append(approx)
        return result
    
    def find_gates(self, cnt):
        result = []
        for gate in cnt:
            hull = cv2.convexHull(gate)
            approx = cv2.approxPolyDP(hull,0.01*cv2.arcLength(hull,True),True)
            
            if len(approx) in (4,5):
                result.append(approx)
                if self.draw_other:
                    cv2.drawContours(self.out, [approx], -1, self.YELLOW, 2, lineType=8)
            
            if self.draw_c2:
                cv2.drawContours(self.out, [approx], -1, self.BLUE, 2, lineType=8)
        
        return result

    def quad_normals(self, img):
        
        self.result = result = []
        
        if not self.enabled:
            self.target_present = False
            return img
        
        now = time.time()
        
        if self.logging_enabled:
            self.storage.set_image(img)
        
        self.preallocate(img)
        
        cnt = self.find_contours(img)
        gates = self.find_gates(cnt)
        
        h, w = img.shape[:2]
        h = float(h)
        w = float(w)
        
        for q in gates:
            #M = cv2.moments(q)
            #cx = int(M['m10']/M['m00'])
            #cy = int(M['m01']/M['m00'])
            ((cx, cy), (rw, rh), rotation) = cv2.minAreaRect(q)
            
            gate = {}
            gate['d'] = q
            gate['av'] = self.VFOV * cy / h - self.VFOV_2
            gate['ah'] = self.HFOV * cx / w - self.HFOV_2
            
            # experimental distance value.. doesn't work
            gate['ad'] = (self.tcx)/math.tan(math.radians(-gate['av'] + self.camera_pitch))
            result.append(gate)
            
        self.target.clear()
        
        # sort the returned data, tend to prefer the 'closest' gate to the center
        if len(result):
            result.sort(key=lambda k: abs(k['ah']))
            target = result[0]
        
            if self.draw:
                cv2.drawContours(self.out, [target['d']], -1, self.RED, 2, lineType=8)
            
            # angle, height, ts
            self.target += [target['ah'], target['av'], target['ad'], now]
            
        self.nt.putValue('target', self.target)
        
        return self.out

def init_filter():
    '''Function called by mjpg-streamer to initialize the filter'''
    
    # Connect to the robot
    NetworkTable.setIPAddress('127.0.0.1')
    NetworkTable.setClientMode()
    NetworkTable.initialize()
    
    #os.system("v4l2-ctl -d /dev/video1 -c exposure_auto=1 -c exposure_absolute=20")
    #os.system("v4l2-ctl -d /dev/video2 -c exposure_auto=1 -c exposure_absolute=10")
    
    filter = TargetFinder()
    return filter.quad_normals
