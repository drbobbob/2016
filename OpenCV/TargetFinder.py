import cv2
import numpy as np
import os
import sys

class TargetFinder(object):
    VFOV = 90 # Camera's vertical field of view
    HFOV = 120 # Camera's horizontal field of view

    def find_contours(self, img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 75, 255, cv2.THRESH_BINARY)
        contours, h = cv2.findContours(thresh, 1, 2)
        result = []
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            if len(approx)>5 and len(approx)<10:
                x,y,w,h = cv2.boundingRect(approx)
                if w > 25:      
                    result.append(approx)
        return result
    
    def find_gates(self, cnt):
        result = []
        for gate in cnt:
            hull = cv2.convexHull(gate)
            approx = cv2.approxPolyDP(hull,0.01*cv2.arcLength(hull,True),True)
            if len(approx) == 4:
                result.append(approx)
        return result

    def quad_normals(self, img):
        cnt = self.find_contours(img)
        gates = self.find_gates(cnt)
        result = []
        for q in gates:
            M = cv2.moments(q)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            gate = {}
            gate['av'] = self.VFOV * cx / float(img.shape[1]) - self.VFOV/2
            gate['ah'] = self.HFOV * cy / float(img.shape[0]) - self.HFOV/2
            result.append(gate)
        return result
