#!/usr/bin/env python3

import os
import sys
import cv2
import TargetFinder

from networktables import NetworkTable


class StaticTester:
    
    settings = [] + \
        ['thresh_%s' % t for t in
         ['hue_p', 'hue_n', 'sat_p', 'sat_n', 'val_p', 'val_n']]
    
    def __init__(self):
        
        NetworkTable.initialize()
        self.tf = TargetFinder.TargetFinder()
        self.tf.enabled = True
        
        cv2.namedWindow('img')
    
        for s in self.settings:
            self._create_trackbar(s)
            
    def _create_trackbar(self, n):
        cv2.createTrackbar(n, 'img', getattr(self.tf, n), 255, lambda v: self._on_change(n, v))
    
    def _on_change(self, n, v):
        setattr(self.tf, n, v)
        self.process()
        
    def process(self):
        
        out_img = self.tf.quad_normals(self.current)
        out = self.filename+', '
        for normal in self.tf.result:
            out += '%.2f, %.2f %.2f' % (normal['av'], normal['ah'], normal['ad'])
            
        print(' '.join(str(getattr(self.tf, s)) for s in self.settings))
            
        print(out)
        
        cv2.imshow('img', out_img)
        #cv2.imshow('bin', self.tf.bindbg)
    
    def run(self, files):
        print("filename, vertical angle, horizontal angle")
        idx = 0
        direction = 1
        while True:
            idx = min(len(files)-1, max(idx, 0))
            
            filename = files[idx]
            img = cv2.imread(filename)
            if img is not None:
                self.filename = filename
                self.current = img
                
                self.process()
                
                key = cv2.waitKey(0) & 0xff
                if key == 0x1b: # ESC key
                    cv2.destroyAllWindows()
                    break
                
                direction = -1 if key == 2 else 1
            
            idx += direction

if __name__ == "__main__":
    
    files = list(os.path.join(sys.argv[1], p) for p in os.listdir(sys.argv[1]))
    
    StaticTester().run(files)
