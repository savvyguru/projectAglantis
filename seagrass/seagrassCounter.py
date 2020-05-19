import cv2
import argparse
import copy
import os
import sys
#cofiguration
#6.2 too high
THRESHOLD = 6.4

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

def isSeagrass(blue,green,red,threshold):
    try:
        #if green >THRESHOLD and (green > red and green > blue):
        #    return True
        #visible spectral-index based strategy
        #citation: http://iranarze.ir/wp-content/uploads/2018/03/E6087-IranArze.pdf
        rgb = blue + green + red
        r = red/rgb
        b = blue/rgb
        g = green/rgb
        ExG = 2*g - r -b
        ExGR = ExG - (1.4*r-g)
        denominator = (r**0.667)*(b**0.333)
        print(denominator)
        VEG = g/denominator
        CIVE = 0.441*r - 0.881*g + 0.385*b + 18.78745
        #COM is the combined index
        COM = 0.25*ExG + 0.30*ExGR + 0.33*CIVE + 0.12*VEG
        if COM > threshold:
            return True
        return False
    except:
        print("Error in isSeagrass() function")
        
def percentageSeagrass(seagrassPixels,totalPixel):
    return (seagrassPixels/totalPixel)*100
    
    
def main():
    seagrassPixels = 0
    failCounter = 0
    #read image as (blue,green,red) values
    img = cv2.imread(args["image"],1)
    (rows,cols,color) = img.shape
    totalPixel = rows * cols
    retImage = copy.deepcopy(img)
    #read pixel one by one
    for j in range(cols):
        for i in range(rows):
            try:
                blue = img[i,j,0]
                green = img[i,j,1]
                red = img[i,j,2]
                if isSeagrass(blue,green,red,THRESHOLD)==True:
                    seagrassPixels += 1
                    #return image with blacked out green pixels
                    retImage[i,j,0] = 0
                    retImage[i,j,1] = 0
                    retImage[i,j,2] = 0
            except:
                failCounter += 1
                
    #output percentage of seagrass
    percentage = round(percentageSeagrass(seagrassPixels,totalPixel),2)
    percentageString = "Percentage of seagrass is "+str(percentage)+"%"
    print(percentageString)
    #print(failCounter)
    
    #save image
    filename = 'savedImage.jpg'
    #display retImage
    if totalPixel > 1000000:
        imS = cv2.resize(retImage, (960, 540))
        cv2.imwrite(filename, imS)
        cv2.imshow("PIC", imS)
    else:
        cv2.imwrite(filename, retImage)
        cv2.imshow("PIC",retImage)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    sys.exit(0)
    
if __name__ == "__main__":
    main()
