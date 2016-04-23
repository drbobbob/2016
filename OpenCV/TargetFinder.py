'''
    Can run this on the roborio by executing mjpg-streamer like so:

    mjpg_streamer -i 'input_opencv.so -r 320x240 --fps 15 --quality 30 --filter /usr/local/lib/mjpg-streamer/cvfilter_py.so --fargs /home/admin/TargetFinder.py'
'''

import cv2
import numpy as np
import os
import os.path
import shutil
import sys
import threading
import time

from networktables import NetworkTable
from networktables.util import ntproperty


class Storage:
    
    location = '/media/sda1/camera'
    
    logging_error = ntproperty('/camera/logging_error', False, writeDefault=True)
    capture_period = ntproperty('/camera/capture_period', 1.0)
    
    def __init__(self):
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
            
    
    def _run(self):
        
        last = time.time()
        
        print("Thread started")
        
        if not os.path.exists(self.location):
            print("Oops")
            self.logging_error = True
            return
        
        self.logging_error = False
        
        self.location = self.location + '/%s' % time.strftime('%Y-%m-%d %H.%M.%S')
        os.makedirs(self.location, exist_ok=True)
        
        while True:
            with self.lock:
                now = time.time()
                while (not self.has_image) or (now - last) < self.capture_period:
                    self.lock.wait()
                    now = time.time()
                    
                self.out2, self.out1 = self.out1, self.out2
                self.has_image = False
            
            
            fname = '%s/%.2f.jpg' % (self.location, now)
            #print("Writing", fname)
            cv2.imwrite(fname, self.out2)
            
            last = now
    
class TargetFinder:
    
    # Values for the lifecam-3000
    VFOV = 34.3 # Camera's vertical field of view
    HFOV = 61 # Camera's horizontal field of view
    
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)
    BLUE = (255, 0, 0)
    MOO = (255, 255, 0)
    
    colorspace = cv2.COLOR_BGR2HSV
    
    enabled = ntproperty('/camera/enabled', False)
    logging_enabled = ntproperty('/camera/logging_enabled', False)
    
    min_width = ntproperty('/camera/min_width', 20)
    #intensity_threshold = ntproperty('/camera/intensity_threshold', 75)
    
    target_present = ntproperty('/components/autoaim/present', False)
    target_angle = ntproperty('/components/autoaim/target_angle', 0)
    target_height = ntproperty('/components/autoaim/target_height', 0)

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
    draw_hue = ntproperty('/camera/draw_hue', False)
    draw_sat = ntproperty('/camera/draw_sat', False)
    draw_val = ntproperty('/camera/draw_val', False)
    
    def __init__(self):
        self.size = None
        self.storage = Storage()
        
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
        
        for i, cnt in enumerate(contours):
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
                if self.draw:
                    cv2.drawContours(self.out, [approx], -1, self.YELLOW, 2, lineType=8)
            
            if self.draw_c2:
                cv2.drawContours(self.out, [approx], -1, self.BLUE, 2, lineType=8)
        
        return result

    def quad_normals(self, img):
        
        self.result = result = []
        
        if not self.enabled:
            self.target_present = False
            return img
        
        if self.logging_enabled:
            self.storage.set_image(img)
        
        self.preallocate(img)
        
        cnt = self.find_contours(img)
        gates = self.find_gates(cnt)
        
        h, w = img.shape[:2]
        h = float(h)
        w = float(w)
        
        for q in gates:
            M = cv2.moments(q)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            gate = {}
            gate['d'] = q
            gate['av'] = self.VFOV * cy / h - self.VFOV/2
            gate['ah'] = self.HFOV * cx / w - self.HFOV/2
            result.append(gate)
        
        # sort the returned data, tend to prefer the 'closest' gate to the center
        if len(result):
            result.sort(key=lambda k: abs(k['ah']))
            target = result[0]
        
            if self.draw:
                cv2.drawContours(self.out, [target['d']], -1, self.RED, 2, lineType=8)
        
            self.target_present = True
            self.target_angle = target['ah']
            self.target_height = target['av']
        else:
            self.target_present = False
            # don't set angle
        
        return self.out

def init_filter():
    '''Function called by mjpg-streamer to initialize the filter'''
    
    # Connect to the robot
    NetworkTable.setIPAddress('127.0.0.1')
    NetworkTable.setClientMode()
    NetworkTable.initialize()
    
    os.system("v4l2-ctl -d /dev/video1 -c exposure_auto=1 -c exposure_absolute=20")
    os.system("v4l2-ctl -d /dev/video2 -c exposure_auto=1 -c exposure_absolute=10")
    
    filter = TargetFinder()
    return filter.quad_normals
