#!/usr/bin/env python3

import os
import sys
import cv2
import TargetFinder

from networktables import NetworkTable


def main():
    
    NetworkTable.initialize()
    
    tf = TargetFinder.TargetFinder()
    print("filename, vertical angle, horizontal angle")
    for filename in os.listdir(sys.argv[1]):
        filename = os.path.join(sys.argv[1], filename)
        img = cv2.imread(filename)
        if img is None:
            continue
        
        out_img = tf.quad_normals(img)
        out = filename+', '
        for normal in tf.result:
            out += '%.2f, %.2f ' % (normal['av'], normal['ah'])
        print(out)
        
        if True:
            cv2.imshow('img',out_img)
            key = cv2.waitKey(0) & 0xff
            if key == 0x1b: # ESC key
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    main()
