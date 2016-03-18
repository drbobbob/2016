'''
    Can run this on the roborio by executing mjpg-streamer like so:

    mjpg_streamer -i 'input_opencv.so -r 320x240 --fps 15 --quality 30 --filter /usr/local/lib/mjpg-streamer/cvfilter_py.so --fargs /home/admin/TargetFinder.py'
'''

import cv2
import numpy as np
import os
import sys

from networktables import NetworkTable
from networktables.util import ntproperty

class TargetFinder:
    
    # Values for the lifecam-3000
    VFOV = 34.3 # Camera's vertical field of view
    HFOV = 61 # Camera's horizontal field of view
    
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)
    BLUE = (255, 0, 0)
    
    enabled = ntproperty('/camera/enabled', False)
    
    min_width = ntproperty('/camera/min_width', 25)
    intensity_threshold = ntproperty('/camera/intensity_threshold', 75)
    draw = ntproperty('/camera/draw', True)
    
    target_present = ntproperty('/components/autoaim/present', False)
    target_angle = ntproperty('/components/autoaim/target_angle', 0)
    target_height = ntproperty('/components/autoaim/target_height', 0)

    def __init__(self):
        self.size = None
        
    def preallocate(self, img):
        if self.size is None or self.size[0] != img.shape[0] or self.size[1] != img.shape[1]:
            h, w = img.shape[:2]
            self.size = (h, w)
            
            # these are preallocated so we aren't allocating all the time
            self.gray = np.empty((h, w, 1), dtype=np.uint8)
            self.thresh = np.empty((h, w, 1), dtype=np.uint8)
            self.out = np.empty((h, w, 3), dtype=np.uint8)
            
        # Copy input image to output
        cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=self.RED, dst=self.out)

    def find_contours(self, img):
        cv2.cvtColor(img,cv2.COLOR_BGR2GRAY, dst=self.gray)
        ret, _ = cv2.threshold(self.gray, self.intensity_threshold, 255, cv2.THRESH_BINARY, dst=self.thresh)
        _, contours, h = cv2.findContours(self.thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        result = []
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx)>5 and len(approx)<10:
                x,y,w,h = cv2.boundingRect(approx)
                if w > self.min_width:      
                    result.append(approx)
        return result
    
    def find_gates(self, cnt):
        result = []
        for gate in cnt:
            hull = cv2.convexHull(gate)
            approx = cv2.approxPolyDP(hull,0.01*cv2.arcLength(hull,True),True)
            if len(approx) == 4:
                result.append(approx)
                if self.draw:
                    cv2.drawContours(self.out, [approx], -1, self.YELLOW, 2, lineType=8)
        return result

    def quad_normals(self, img):
        
        self.result = result = []
        
        if not self.enabled:
            self.target_present = False
            return img
        
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

    # requires v4l-utils installed on roborio
    try:
        import sh

        getattr(sh, 'v4l2-ctl')('-c', 'exposure_auto=1',
                                '-c', 'exposure_absolute=10')
    except:
        pass
    
    filter = TargetFinder()
    return filter.quad_normals
