# -*- coding: utf-8 -*-

import cv2
from cvzone import HandTrackingModule

capture = cv2.VideoCapture(0)
detector = HandTrackingModule.HandDetector(maxHands=2)
while True:
        success, img =capture.read()
        hands, img = detector.findHands(img)
        #inside the returned hand value we can get all details about  the hand bounding, etc.
        
        cv2.imshow("Hands Detetcted", img)
        
        if(hands):
            # Hand 1
            hand1 = hands[0]
            myHandType = hand1["type"]
            if(myHandType == "Right"):
                print("Quitting...")
                cv2.waitKey(2000)
                capture.release()
                cv2.destroyAllWindows()
            if(myHandType == "Left"):
                print("Next Page...")
                from QrCodeScanner import main
                break
        #each 1ms it will check if you pressed on x keyboard, if yes it will break the loop
        cv2.waitKey(1)
        #if myHandType == "Right":
            #break
capture.release()
cv2.destroyAllWindows()