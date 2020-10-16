import cv2
import argparse
import os
import sys
import math
import warnings
import numpy as np
import copy

#ignore divide by zero warnings in isSeagrass()
warnings.filterwarnings("ignore")
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())
   
def main():
    seagrassPixels = 0
    #read image as (blue,green,red) values
    img = cv2.imread(args["image"],1)
    blue = img[:,:,0]
    green = img[:,:,1]
    red = img[:,:,2]
    rgb = blue+red+green
    b = blue / rgb
    r = red / rgb
    g = green / rgb
    ExG = 2*g - r -b
    part1 =r**0.667
    part2 = b**0.333
    denominator = part1*part2
    VEG = g/denominator
    CIVE = 0.441*r - 0.881*g + 0.385*b + 18.78745
    COM2 = 0.36*ExG + 0.47*CIVE + 0.17*VEG
    threshold = COM2 > 9
    retR = red * threshold
    retG = green * threshold
    retB = blue * threshold
    retImage = copy.deepcopy(img)
    retImage[:,:,0] = retB
    retImage[:,:,1] = retG
    retImage[:,:,2] = retR
    
    pixels = np.sum(threshold)
    h, w, c = img.shape
    totalPixel = h*w
    percentage = round(pixels*100/totalPixel,2)
    percentageString = "Percentage of seagrass is "+str(percentage)+"%"
    print(percentageString)
    filename = 'savedImage.jpg'
    newsize = 960*540
    scalefactor = int(math.sqrt(totalPixel/newsize))
    if totalPixel > 1000000:
        imS = cv2.resize(retImage, (int(w/scalefactor), int(h/scalefactor)))
        cv2.imwrite(filename, imS)
    else:
        cv2.imwrite(filename, retImage)
    
if __name__ == "__main__":
    main()
