import cv2
import numpy as np
import predict
import os,cv2
import sys,argparse
import numpy as np


dir_path = os.path.dirname(os.path.realpath(__file__))
image_path=sys.argv[1] 
filename = dir_path +'/' +image_path
#import image
image = cv2.imread(filename)
#cv2.imshow('orig',image)
#cv2.waitKey(0)

#grayscale
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow('gray',gray)
cv2.waitKey(0)

#binary
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
cv2.imshow('second',thresh)
cv2.waitKey(0)

#dilation
kernel = np.ones((5,5), np.uint8)
img_dilation = cv2.dilate(thresh, kernel, iterations=1)
#cv2.imshow('dilated',img_dilation)
#cv2.waitKey(0)

#find contours
_,ctrs,_ = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#sort contours
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
a = np.zeros(shape=(10,4))
print(a)

for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    
    x, y, w, h = cv2.boundingRect(ctr)
    print(i)
    print(x)
    print(y)
    print(w)
    print(h)
    a[i]=[x,y,w,h]



    # Getting ROI
   # roi = image[y:y+h, x:x+w]

    # show ROI
    #cv2.imshow('segment no:'+str(i),roi)
    #cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
    #cv2.waitKey(0)


for l in range(0,i):
	if(abs(a[l+1][0]-a[l][0])<=50):
		xmin=min(a[l][0],a[l+1][0])
		print(xmin)
		xmax=max(a[l][0]+a[l][2],a[l+1][0]+a[l+1][2])
		print(xmax)

		ymin=min(a[l][1],a[l+1][1])
		print(ymin)

		ymax=max(a[l][1]+a[l][3],a[l+1][1]+a[l+1][3])
		print(ymax)

		print("hello")
		
		a[l][0]=xmin
		a[l][1]=ymin
		a[l][2]=xmax-xmin
		a[l][3]=ymax-ymin

		a[l+1][0]=a[l+2][0]
		a[l+1][1]=a[l+2][1]

		a[l+1][2]=a[l+2][2]

		a[l+1][3]=a[l+2][3]
		a[l+2]=[0,0,0,0]
		i=i-1
		print (a)


ans=""
for l in range (0,i+1):
	l,m,n,o=a[l]
	x=int(l)
	y=int(m)
	w=int(n)
	h=int(o)

	roi = image[y:y+h, x:x+w]
	dim=(60,30)
	resized = cv2.resize(roi, dim, interpolation = cv2.INTER_AREA)
	cv2.imshow('l',resized)
	cv2.waitKey(0)
	ans=ans+" "+predict.find_class(resized)


	#cv2.imshow('segment no:'+str(i),roi)
	#cv2.rectangle(image,(x,y),( x + w, y + h ),(90,0,255),2)
	#cv2.waitKey(0)

print(i)

#cv2.imshow('marked areas',image)
print(ans)
cv2.waitKey(0)