# vision-logo

Notes: 

Update as of November 25th: It turns out the feature-matching works great on complex logos with text and stuff, but works poorly on simple logos like the Nike swoosh. Currently working on a hybrid solution that combines an advanced version of template matching with feature-matching. It doesn't work yet, hence I'm not pushing it to the github right now.



test.py just plays with a static image

FMtester.py contains a working solution for feature-matching an image using a webcam that feeds realtime information. The brute-force algorithm for matching is in cv2.ORB()

More efficient algorithms can be used with SIFT however it is not included in the standard OpenCV package

Feature-matching generally works for complex logos and is able to pick the best match 
