import cv2
import argparse
import copy
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

def isSeagrass(h):
    #citation: https://www.sciencedirect.com/science/article/pii/S2214317315000347
    #key idea: hue of pixel independent of the brightness of the image
    #clasify as seagrass if within upper and lower hue threshold for green
    if  50<h<200:
        #print("green pixel")
        return True
    return False

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
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #read pixel one by one
    for j in range(cols):
        for i in range(rows):
            try:
                smallImg = img[i,j]
                print("rbg",retImage[i,j])
                print("hsv",smallImg)
                if isSeagrass(h)==True:
                    seagrassPixels += 1
                    #return image with blacked out green pixels
                    retImage[i,j,0] = 0
                    retImage[i,j,1] = 0
                    retImage[i,j,2] = 0
            except:
                failCounter += 1
                print("failed")
                
    #output percentage of seagrass
    percentage = round(percentageSeagrass(seagrassPixels,totalPixel),2)
    print(percentage,"%")
    print("failcounter",failCounter)
    #display retImage
    
    #resize image if output image is too large
    if totalPixel > 1000000:
        imS = cv2.resize(retImage, (960, 540))
        cv2.imshow("GreenAsBlack", imS)
    else:
        cv2.imshow("GreenAsBlack",retImage)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    sys.exit()
    
if __name__ == "__main__":
    main()

