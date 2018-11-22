import cv2
import math
import numpy as np
#from matplotlib import pyplot as plt

img = cv2.imread("ultimo_sopravvissuto.jpg", cv2.IMREAD_GRAYSCALE) # queryiamge

cap = cv2.VideoCapture(0)

# Features
orb = cv2.ORB_create()
kp_image, desc_image = orb.detectAndCompute(img, None)

# Feature matching
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
done = False

while not done:
    _, frame = cap.read()
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # trainimage

    thing = orb.detectAndCompute(grayframe, None)

    kp_grayframe, desc_grayframe = thing
    if desc_grayframe is not None:
        matches = matcher.match(desc_image, desc_grayframe)
        matches = sorted(matches, key = lambda x:x.distance)
    else:
        matches = []

    matchesLength = math.ceil(len(matches)*.1)#takes top 10% of matches in []
    matching_result = cv2.drawMatches(img, kp_image, grayframe, kp_grayframe, matches[:matchesLength], None, flags=2)
    cv2.imshow("matching", matching_result)

    key = cv2.waitKey(1)
    if key == 27:
        done = True

cap.release()
cv2.destroyAllWindows()

