import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy



wcam, hcam = 640, 480
framR=100
smothing=6
plocX,plocY = 0,0
clocX,clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4,hcam)

ptime = 0
detector = htm.handDetector(maxHands=1)
wscr , hscr = autopy.screen.size()

cv2.namedWindow("AI mouse", cv2.WINDOW_NORMAL)
cv2.resizeWindow("AI mouse",1500, 1100)

while True:

    success , img =cap.read()
    img =detector.findHands(img)
    lmList,bbox=detector.findPosition(img)

    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        # print(x1,y1,x2,y2)

        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (framR, framR), (wcam - framR, hcam - framR), (255, 0, 255), 2)

        if fingers[1]==1 and fingers[2]==0:
            x3=np.interp(x1,(framR,wcam-framR),(0,wscr))
            y3=np.interp(y1,(framR,hcam-framR),(0,hscr))
            clocX=plocX+(x3-plocX)/smothing
            clocY=plocY+(y3-plocY)/smothing

            autopy.mouse.move(wscr-clocX,clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY=clocX,clocY

        if fingers[1]==1 and fingers[2]==1:
            length,img,info=detector.findDistance(8,12,img)
            # print(length)
            if length<40:
                cv2.circle(img,(info[4],info[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()
                time.sleep(0.2)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)


    cv2.imshow("AI mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


