import cv2
import numpy as np
import tkinter as tk



#webcamp config
capture = cv2.VideoCapture(cv2.CAP_DSHOW);

#image target config
imgTarget = cv2.imread("targetimage.jpg")
imgTarget = cv2.resize(imgTarget, (540, 540)) 
ht, wt, ct = imgTarget.shape

#image to display
trainImg = cv2.imread("train.png")
trainImg = cv2.resize(trainImg, (540, 540)) 

#displayed cordinates
position = (10,50)


#orb detector configuration (to put detectors on the image target)
orb = cv2.ORB_create(100000)

kp1, des1 = orb.detectAndCompute(imgTarget,None)
imgTarget = cv2.drawKeypoints(imgTarget, kp1, None)

#matcher:
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#webcam
while True:
    sucess, imgWebcam = capture.read();
    
    #generate keypoints for camrea display too
    #kp2, des2 = orb.detectAndCompute(imgWebcam,None)
    kp2, des2 = orb.detectAndCompute(imgWebcam,None)
    imgWebcam = cv2.drawKeypoints(imgWebcam, kp2, None)
    
    #we will compare both keypoints of camera and image target
    #if they were the same so conditions verified thus we can display th result ontop
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
    matches = matcher.knnMatch(des1, des2, 2)
    matched1 = []
    matched2 = []
    nn_match_ratio = 0.8  # Nearest neighbor matching ratio
    for m, n in matches:
        if m.distance < nn_match_ratio * n.distance:
            matched1.append(kp1[m.queryIdx])
            matched2.append(kp2[m.trainIdx])
    
    #declare list contains good matches between the two
    good_matches = [] 
    for m,n in matches:
        if m.distance < 0.68*n.distance:
            #then its a good macth
            good_matches.append(m)
    print(len(good_matches))
    
    #draw matchers
    imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good_matches, None, flags=2 )
    
    if len(good_matches)>20:
        imgWebcam = cv2.putText(imgWebcam,"hello world!",position,cv2.FONT_HERSHEY_SIMPLEX,1#fontsize
                                ,(0,255,0),3)
        
    #display both image and webcam
    cv2.imshow('Image Features',imgFeatures)
    cv2.imshow('Image Target',imgTarget)
    cv2.imshow('Train Image',trainImg)
    cv2.imshow('Webcam',imgWebcam)
    cv2.waitKey(1)
