#This code works assuming that the hand is in the centre of the picture
import cv2
import numpy as np
import matplotlib.pyplot as plt 
#Reading the pic and converting to HSV
i=cv2.imread(" ")
img=cv2.cvtColor(i,cv2.COLOR_BGR2HSV)
#Rectangle at the centre of the picture
a=img.shape[1]/2-5
b=img.shape[1]/2+5
c=img.shape[0]/2-5
d=img.shape[0]/2+5
#ROI
img2=img[c:d,a:b]
#Creating histogram of ROI and normalizing it
imghist=cv2.calcHist([img2],[0],None,[69],[0,180])
cv2.normalize(imghist,imghist,0,180,cv2.NORM_MINMAX)
#Back projection
img3=cv2.calcBackProject([img],[0],imghist,[0,180],3)
#Thresholding to 255 as scale is 3 in previous step
ret,thresh = cv2.threshold(img3,254,255,0)
thresh = cv2.merge((thresh,thresh,thresh))
#Convolving 
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))
cv2.filter2D(thresh,-1,disc,thresh)
#Bitwise and
final = cv2.bitwise_and(i,thresh)
cv2.imshow("NailedIt",final)
cv2.waitKey(0)
