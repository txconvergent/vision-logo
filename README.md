# vision-logo

Notes: 

test.py just plays with a static image

FMtester.py contains a working solution for feature-matching an image using a webcam that feeds realtime information. The brute-force algorithm for matching is in cv2.ORB()

More efficient algorithms can be used with SIFT however it is not included in the standard OpenCV package

next steps: build a folder full of tester/training images of popular logos and pick the best match using info from the camera
