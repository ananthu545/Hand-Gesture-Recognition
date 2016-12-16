import cv2
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
i=cv2.imread("C:\\Users\Lakshmi\Pictures\Camera Roll\WIN_20161215_194238.JPG")
img=cv2.cvtColor(i,cv2.COLOR_BGR2HSV)
a=img.shape[1]/2-5
b=img.shape[1]/2+5
c=img.shape[0]/2-5
d=img.shape[0]/2+5
#print(a,b,c,d)
img2=img[c:d,a:b]
#cv2.imshow("a",i)
#cv2.waitKey(0)
#plt.imshow(img)
imghist=cv2.calcHist([img2],[0],None,[69],[0,180])
cv2.normalize(imghist,imghist,0,180,cv2.NORM_MINMAX)
img3=cv2.calcBackProject([img],[0],imghist,[0,180],3)
#cv2.imshow("haha",img3)
#cv2.waitKey(0)
#plt.imshow(img3)
ret,thresh = cv2.threshold(img3,254,255,0)
thresh = cv2.merge((thresh,thresh,thresh))
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))
cv2.filter2D(thresh,-1,disc,thresh)
res = cv2.bitwise_and(i,thresh)
cv2.imshow("haha",res)
cv2.waitKey(0)