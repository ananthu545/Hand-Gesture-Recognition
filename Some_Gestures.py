import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
import math
#Camera Start
camera = cv2.VideoCapture(0)
ready=0
hand=0
#Work start
while(1):
    #Getting input from camera,filtering and fliiping it
    ret, frame = camera.read()
    frame=cv2.bilateralFilter(frame,5,10,20)
    frame=cv2.flip(frame,1)
    #Copy of frame
    frame1=np.copy(frame)
    #Data used for displaying ROI rectangles
    a=int(frame.shape[1]/2-20)
    b=int(frame.shape[1]/2+20)
    c=int(frame.shape[0]/2-20)
    d=int(frame.shape[0]/2+20) 
    
  
    # Displaying ROI rectangles
    box_x=np.array([150+a,150+b+20,150+a,150+b+20,150+a,150+b+20],dtype=int)
    box_y=np.array([c,c,d+20,d+20,d+80,d+80],dtype=int)
    for i in range(6):
           cv2.rectangle(frame1,(box_x[i],box_y[i]),(box_x[i]+40,box_y[i]+40),(255,0,0),1)
    frame=frame[0:frame.shape[0],frame.shape[1]/2:frame.shape[1]]
           
 
    #To indicate if you're ready and to capture your hand
    if(ready):
         if(not(hand)):
                 cv2.putText(frame1,"Press H to capture le Hand.",(int(0.05*frame.shape[1]),int(0.97*frame.shape[0])),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,255),1,8) 
          
    else:
                 cv2.putText(frame1,"Press R to begin.",(int(0.05*frame.shape[1]),int(0.97*frame.shape[0])),cv2.FONT_HERSHEY_DUPLEX,2,(0,255,255),1,8) 
        
    #If hand is captured 
    if(hand and ready):
        #Makes a copy of frame,blurring is applied and it is converted to HSV for backrpojection
        frame3=np.copy(frame)
        frame3=cv2.medianBlur(frame3,3)
        hsv=cv2.cvtColor(frame3,cv2.COLOR_BGR2HSV)
        #Backprojection using histogram of hand initially captured
        backproject=cv2.calcBackProject([hsv],[0,1],handhist,[0,180,0,256],1)
        #Convolving and applying different blurs 
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(16,16))
        cv2.filter2D(backproject,-1,disc,backproject)
        backproject=cv2.GaussianBlur(backproject,(11,11), 0)
        backproject=cv2.medianBlur(backproject,3)
        ret,thresh=cv2.threshold(backproject,200,255,0)
        frame=thresh
        

        #Getting and displaying contour of maximum area
        image,contours,hierarchy=cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        convex_hull=cv2.convexHull(cnt)
        #Drawing is just another separate frame which displays the actual contours and convex hull
        drawing=np.ones(frame.shape,np.uint8)
        cv2.drawContours(drawing,[cnt],0,(0,255,0),3)
        cv2.drawContours(drawing,[convex_hull],0,(0,0,255),3)
        #Getting convex hull
        convex_hull=cv2.convexHull(cnt,returnPoints=False)
        #Getting defects from convex hull and contour of maximum area
        defects=cv2.convexityDefects(cnt,convex_hull)
        cv2.drawContours(frame,[cnt],0,(255,255,0),3)
        count=0
        #Getting different defects and getting tuple values
        for i in range(defects.shape[0]):
                  s,e,f,d = defects[i,0]
                  start = tuple(cnt[s][0])
                  end = tuple(cnt[e][0])
                  far = tuple(cnt[f][0])
                  cv2.line(frame,start,end,[255,255,0],4)
                  # Calculating lengths to find angle using cosine rule
                  len1 = sqrt(((start[0] - far[0])**2) + ((start[1] - far[1])**2))
                  len2 = sqrt(((far[0] - end[0])**2) + ((far[1] - end[1])**2))
                  len3 = sqrt(((start[0] - end[0])**2) + ((start[1] - end[1])**2))
                  cos_thetha = ((len2**2) + (len1**2) - (len3**2))/(2*len1*len2)
                  thetha = math.acos(cos_thetha)
                  thetha = math.degrees(thetha) 
                   #Count gets incremented if the angle btween two lines is less than 90 degrees
                  if(thetha<90):
                           count=count+1
                           #Displays the point between two fingers
                           cv2.circle(drawing,far,1,(255,0,0),3)
        #Displays the contours and convex hulls 
        comp=np.hstack((drawing,frame))
        cv2.imshow("Comp",comp)
        
        # Conditions for various gestures
        if(count==2):
                  cv2.putText(frame1,"V for Victory",(int(0.05*frame.shape[1]),int(0.97*frame.shape[0])),cv2.FONT_HERSHEY_DUPLEX,2,(0,255,255),1,8)
        elif(count==3):
                  cv2.putText(frame1,"The Three Muskateers",(int(0.05*frame.shape[1]),int(0.97*frame.shape[0])),cv2.FONT_HERSHEY_DUPLEX,2,(0,255,255),1,8)
        elif(count==4):
                  cv2.putText(frame1,"Foursome ",(int(0.05*frame.shape[1]),int(0.97*frame.shape[0])),cv2.FONT_HERSHEY_DUPLEX,2,(0,255,255),1,8)    
        elif(count==5):
                  cv2.putText(frame1,"Holas Amigos",(int(0.05*frame.shape[1]),int(0.97*frame.shape[0])),cv2.FONT_HERSHEY_DUPLEX,2,(0,255,255),1,8)          
        else:
                  cv2.putText(frame1,"Wondering !!!",(int(0.05*frame.shape[1]),int(0.97*frame.shape[0])),cv2.FONT_HERSHEY_DUPLEX,2,(0,255,255),1,8)    
    
    
    interrupt=cv2.waitKey(10)
    #Key input for various stuff
    #Press q to quit at any time
    if interrupt & 0xFF == ord('q'):
        break
    #Press r to show that you are ready to begin
    elif interrupt & 0xFF == ord('r'):
        ready=1
    #Press h to capture your hand for comparison
    elif interrupt & 0xFF == ord('h'):
        if(ready):
            hand=1
            #Converts colour of captured hand to HSV for histogram creation for backprojection
            hsv=cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)
            ROI=np.zeros([240,40,3],dtype=hsv.dtype)
            for i in range(6):
                      ROI[i*40:i*40+40,0:40]=hsv[box_y[i]:box_y[i]+40,box_x[i]:box_x[i]+40]
            handhist = cv2.calcHist([ROI],[0,1], None, [180,30], [0, 180,0,256])
            #Normalization of histogram
            cv2.normalize(handhist,handhist, 0, 255, cv2.NORM_MINMAX)
   #Displays output
    cv2.imshow("Result",frame1)
#After all work is over, releases cam
camera.release()
cv2.destroyAllWindows()
        
