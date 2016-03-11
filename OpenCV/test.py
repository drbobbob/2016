import os
import sys
import cv2
import TargetFinder

def main():
    tf = TargetFinder.TargetFinder()
    print("filename, vertical angle, horizontal angle")
    for filename in os.listdir(sys.argv[1]):
        filename = os.path.join(sys.argv[1], filename)
        img = cv2.imread(filename)
        normals = tf.quad_normals(img)
        out = filename+', '
        for normal in normals:
            out += normal['av'] + ', ' + normal['ah']
        print(out)
        #cv2.imshow('img',img)
        #if cv2.waitKey(0) & 0xff == 27:
        #    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
