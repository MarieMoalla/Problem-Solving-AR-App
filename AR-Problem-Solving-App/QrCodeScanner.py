import cv2
import numpy as np
from pyzbar.pyzbar import decode
import DbConnector
import tkinter as tk
from cvzone import HandTrackingModule
import threading
import keyboard 
import SendEmail


root=tk.Tk()
root.geometry("700x640")
#%%webcamp config
capture = cv2.VideoCapture(cv2.CAP_DSHOW);
capture.set(3,640)#3; width id
capture.set(4,480)#4: high id
#%%

#detector configuration
detector = HandTrackingModule.HandDetector(maxHands=2)

#%%displayed info cordinates
teamTitlePosition = (10,50)
scorePosition = (10,90)
rankPosition = (10,130)

svpPosition = (10,170)
usvpPosition = (10,210)
waPosition = (10,250)

timerPosition = (10,455)
#%%

def helps_timer():
    threading.Timer(5.0, incriemnt_help).start()
    
def incriemnt_help():
      global helps
      helps = 1  
      
teams = []

def close_program():
    capture.release()
    cv2.destroyAllWindows()

helps=1
teamId=0

def main():
    while True: 
                success, qr = capture.read()
                hands, qr = detector.findHands(qr)
                
                #guide
                cv2.putText(qr,"Press H to Get Help when you raise your hand.",(10,415),cv2.FONT_HERSHEY_SIMPLEX,0.7,(11,255,1),2)
                cv2.putText(qr,"Press X to Exit.",(10,455),cv2.FONT_HERSHEY_SIMPLEX,0.7,(77, 77, 255),2)
                
                #remaining helps guide
                global helps
                if(helps ==1):
                    cv2.putText(qr,"Help Token = 1.",(455,455),cv2.FONT_HERSHEY_SIMPLEX,0.7,(253,254,2),2)
                else:
                    cv2.putText(qr,"Help Token after 5 seconds.",(355,455),cv2.FONT_HERSHEY_SIMPLEX,0.7,(77, 77, 255),2)
                
                global teamId
                if(teamId==0):
                      cv2.putText(qr,"Please Chek in First!",(100,200),cv2.FONT_HERSHEY_SIMPLEX,1.3,(77, 77, 255),2)

                for barcode in decode(qr):
                    
                    #data in byte so we need to decode it
                    myData = barcode.data.decode('utf-8')
                    
                    teamId = myData
                    
                    collection=DbConnector.collection
                    teams = []
                    for x in collection.find():
                         teams.append(x)
                      
                    #after fetching the id we will look for in in our team list
                    #print team name
                    #print(teams[int(myData)-1]["team"])
                    
                    #%%add bounding box for the qr code
                    pts = np.array([barcode.polygon],np.int32)
                    pts = pts.reshape(-1,1,2)
                    cv2.polylines(qr,[pts],True,(255,0,255),5)
                    #%%
                    
                   
                    #%% add team info section
                    try:
                        #id
                        pts2=barcode.rect
                        cv2.putText(qr,"ID: "+str(teams[int(myData)-1]["id"]),(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
                        #team name
                        cv2.putText(qr,"Name: "+teams[int(myData)-1]["team"],teamTitlePosition,cv2.FONT_HERSHEY_SIMPLEX,0.9,(77, 77, 255),2)
                        #team score
                        cv2.putText(qr,"Score: "+str(teams[int(myData)-1]["score"]),scorePosition,cv2.FONT_HERSHEY_SIMPLEX,0.9,(253,254,2),2)
                        #team rank
                        cv2.putText(qr,"Rank: "+str(teams[int(myData)-1]["rank"]),rankPosition,cv2.FONT_HERSHEY_SIMPLEX,0.9,(11,255,1),2)
                        #team ps
                        cv2.putText(qr,"Solved Problems: "+str(teams[int(myData)-1]["solved_problems"]),svpPosition,cv2.FONT_HERSHEY_SIMPLEX,0.9,(11,255,1),2)
                        #team ups
                        cv2.putText(qr,"Unsolved Problems: "+str(teams[int(myData)-1]["unsolved_problems"]),usvpPosition,cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,173,0),2)
                        #team wa
                        cv2.putText(qr,"Wrong Answers: "+str(teams[int(myData)-1]["wrong_answers"]),waPosition,cv2.FONT_HERSHEY_SIMPLEX,0.9,(210,39,48),2)
                        #team timer
                        #cv2.putText(qr,"Timer: "+str(teams[int(myData)-1]["timer"]),timerPosition,cv2.FONT_HERSHEY_SIMPLEX,0.9,(11,255,1),2)
                    
                    except:
                        print("qr code invalide!")
                    #%%
                
                cv2.imshow('Result',qr)
                #refresh each second until you press x(exit)
                if keyboard.is_pressed('x'):
                    break
                #get help
                if keyboard.is_pressed('h'):
                    if(hands):
                        # Hand 1
                        hand1 = hands[0]
                        myHandType = hand1["type"]
                        if(myHandType == "Right" or myHandType == "Left"):
                            
                            if(helps==1):
                                print("current team id:",teamId )
                                print("get help...")
                                #send email
                                SendEmail.send_help("Team Number "+str(teamId)+" need help.")
                                #reset helps
                                helps=0
                                helps_timer()
                                print("helps",helps)
                cv2.waitKey(1)
                           
main()
close_program()
