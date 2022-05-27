import cv2
import numpy as np



#webcamp config
capture = cv2.VideoCapture(cv2.CAP_DSHOW);

#image target config
imgTarget = cv2.imread("targetimage.png")
imgTarget = cv2.resize(imgTarget, (540, 540)) 
ht, wt, ct = imgTarget.shape

#image to display
trainImg = cv2.imread("train.png")
trainImg = cv2.resize(trainImg, (540, 540)) 


#orb detector configuration (to put detectors on the image target)
orb = cv2.ORB_create(nfeatures=1000)
kp1, des1 = orb.detectAndCompute(imgTarget,None)
imgTarget = cv2.drawKeypoints(imgTarget, kp1, None)

#webcam
while True:
    sucess, imgWebcam = capture.read();
    
    #generate keypoints for camrea display too
    kp2, des2 = orb.detectAndCompute(imgWebcam,None)
    imgWebcam = cv2.drawKeypoints(imgWebcam, kp2, None)
    
    #we will compare both keypoints of camera and image target
    #if they were the same so conditions verified thus we can display th result ontop
    #matcher:
    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(des1, des2, k=2)
    
    #declare list contains good matches between the two
    good_matches = [] 
    for m,n in matches:
        if m.distance < 0.75 *n.distance:
            #then its a good macth
            good_matches.append(m)
    print(len(good_matches))
    #draw matchers
    imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good_matches, None, flags=2 )
    #find the homography(the bounding box that surround in our webcam to overlay the image)
    #goal try to find relation between src and dest points (input) ==> matrix (output)
    
    if len(good_matches)>20:
        srcPoints = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        destPoints = np.float32([kp2[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        
        matrix, mask = cv2.findHomography(srcPoints,destPoints,cv2.RANSAC,5)
        print(matrix)
        
        pts = np.float32([[0,0],[0,ht],[wt,ht],[wt,0]]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,matrix)
        img2 = cv2.polylines(imgWebcam,[np.int32(dst)],True,(255,0,255),3)
        
        imgWarp = cv2.warpPerspective(trainImg, matrix, (imgWebcam.shape[1],imgWebcam.shape[0]))
        
        
    #display both image and webcam
    cv2.imshow('Image warp',imgWarp)
    cv2.imshow('Image Features',imgFeatures)
    cv2.imshow('Image Target',imgTarget)
    cv2.imshow('Train Image',trainImg)
    cv2.imshow('Image 2',img2)
    cv2.imshow('Webcam',imgWebcam)
    cv2.waitKey(0)