import cv2
import math
import glob
import webbrowser
import argparse
import sys
import numpy as np

DEFAULT_WIDTH = 500
MATCH_TEMP_WIDTH = 100
MINIMUM_MATCHES = 42

logos = []
descriptions = []
for filepath in glob.glob('logos\*'):
    print(filepath)
    logos.append(cv2.imread(filepath))

descriptions.append("https://www.adidas.com/us")
descriptions.append("https://www.apple.com/")
descriptions.append("http://www.txconvergent.org/")
descriptions.append("http://www.txconvergent.org/")
descriptions.append("https://www.microsoft.com/en-us/")
descriptions.append("https://www.microsoft.com/en-us/")
descriptions.append("https://www.nike.com")
descriptions.append("https://www.samsung.com/us/")
descriptions.append("https://www.samsung.com/us/")
descriptions.append("https://www.spotify.com/us/")
descriptions.append("https://www.underarmour.com/en-us/")


#np_frame = np.asarray(logos)

#construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-t", "--template", required=True, help="Path to template image")
# ap.add_argument("-i", "--images", required=True, help="Path to images where template will be matched")
# ap.add_argument("-v", "--visualize", help="Flag indicating whether or not to visualize each iteration")
# args = vars(ap.parse_args())

# for image in np_frame:
#     print(image)
print(len(logos))
#cv2.namedWindow("output", cv2.WINDOW_NORMAL)

initimg = cv2.imread("init.png")
cv2.imshow("LogoMeNOW",initimg)
cv2.waitKey(3000)
cv2.destroyAllWindows()

stockimg = cv2.imread("nomatches.png") # queryiamge
height, width = stockimg.shape[:2]
scaleFactor0 = DEFAULT_WIDTH/width
stockimg = cv2.resize(stockimg, None, fx=scaleFactor0, fy=scaleFactor0, interpolation = cv2.INTER_LINEAR)

cap = cv2.VideoCapture(0)

# Features
orb = cv2.ORB_create()
#kp_image, desc_image = orb.detectAndCompute(img, None)

# Feature matching
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
done = False

print(orb.getPatchSize())
print(orb.getEdgeThreshold())

orb.setPatchSize(31)
orb.setEdgeThreshold(29)

print(orb.getPatchSize())
print(orb.getEdgeThreshold())

coeff = .18
while not done:
    _, frame = cap.read()
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # trainimage

    kp_grayframe, desc_grayframe = orb.detectAndCompute(grayframe, None)

    #matchesList = []
    bestMatches = []
    imgToShow = stockimg
    kpToShow = orb.detect(stockimg, None)
    logoIndex = -1
    if desc_grayframe is not None:
        min = MINIMUM_MATCHES
        for i in range(len(logos)):
            img = logos[i]
            height, width = img.shape[:2]
            tempimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            scaleFactor2 = DEFAULT_WIDTH/width #change size to desired size
            colortemplate = cv2.resize(img, None, fx=scaleFactor2, fy=scaleFactor2, interpolation = cv2.INTER_LINEAR)
            template = cv2.resize(tempimg, None, fx=scaleFactor2, fy=scaleFactor2, interpolation = cv2.INTER_LINEAR)
            kp_image, desc_image = orb.detectAndCompute(template, None)

            tempMatches = matcher.match(desc_image, desc_grayframe)
            tempMatches = sorted(tempMatches, key = lambda x:x.distance)
            sum = 0;
            if len(tempMatches)>3:
                for idx, val in enumerate(tempMatches):
                    if(idx>math.ceil(len(tempMatches)*coeff)):
                        break

                    sum+=val.distance

                avg = sum/idx
                if(avg<min):
                    min = avg
                    bestMatches = tempMatches
                    imgToShow = colortemplate
                    kpToShow = kp_image
                    logoIndex = i

            #matchesList.append(tempMatches)

    matchesLength = math.ceil(len(bestMatches)*coeff)#takes top 10% of matches in []
    #height, width = imgToShow.shape[:2]
    #scaleFactor2 = 400 / width #400 is default width

    #res = cv2.resize(imgToShow, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
    #kp_final = orb.detect(res, None)
    matching_result = cv2.drawMatches(imgToShow, kpToShow, frame, kp_grayframe, bestMatches[:matchesLength], None, flags=2)
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (650,450)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2

    cv2.putText(matching_result,'press enter to search',
    bottomLeftCornerOfText,
    font,
    fontScale,
    fontColor,
    lineType)
    cv2.imshow("LogoMeNOW", matching_result)
    #cap.release()

    key = cv2.waitKey(1)
    if key==13:
        print("key pressed")
        # Create a black image
        canvas = np.zeros((200,512,3), np.uint8)

        # Write some Text

        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,30)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2

        #Display the image

        if(logoIndex == -1):
            cv2.putText(canvas,'Error: no matches found',
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            lineType)
            cv2.imshow("img",canvas)

        else:
            webbrowser.open(descriptions[logoIndex], True)


    elif key == 27:
        done = True

cap.release()
cv2.destroyAllWindows()

