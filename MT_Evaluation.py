import cv2
from matplotlib import pyplot as plt
import serial
import time
from PIL import Image
import numpy as np

'''arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data'''

def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2), dtype = np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis = 1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew

def bubbleSort(arr):
    
    if arr[0][1] > arr[1][1]:
        arr[0], arr[1] = arr[1], arr[0]
    if arr[1][1] > arr[2][1]:
        arr[1], arr[2] = arr[2], arr[1]
    if arr[2][1] > arr[3][1]:
        arr[2], arr[3] = arr[3], arr[2]

    if arr[0][1] > arr[1][1]:
        arr[0], arr[1] = arr[1], arr[0]
    if arr[1][1] > arr[2][1]:
        arr[1], arr[2] = arr[2], arr[1]

    if arr[0][1] > arr[1][1]:
        arr[0], arr[1] = arr[1], arr[0]
     
imagelist = []
im = 0

coordinates = -1

def findPage(img, num):

    global im
    r,c,p = img.shape

    #cv2.imshow('image', img)

    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray,(5,5),0)
    
    edges = cv2.Canny(img,90,180)

    edges_dil = cv2.dilate(edges,(4,4), iterations=2)

    #cv2.imshow('gray', gray)
    #cv2.imshow('gaussianBlur', blur)

    #cv2.imshow('canny_edges', edges)
    #cv2.imshow('after_dilation', edges_dil)

    contours,hi = cv2.findContours(edges_dil,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) # see the last argument

    mx = 0
    X,Y,W,H = 0,0,0,0

    for contour in contours:

        x,y,w,h = cv2.boundingRect(contour)

        if(w*h > mx):

            epsilon = 0.1*cv2.arcLength(contour,True)
            coordinates = cv2.approxPolyDP(contour,epsilon,True)

            if(len(coordinates)!=4):
                continue

            mx = w*h
            X,Y,W,H = x,y,w,h

    '''corners = coordinates.reshape((4,2))

    print(corners)
    print(len(corners))

    bubbleSort(corners)
    
    if(corners[1][0] < corners[0][0]):
        corners[0], corners[1] = corners[1], corners[0]

    if(corners[3][0] < corners[2][0]):
        corners[2], corners[3] = corners[3], corners[2]

    print("after sorting")

    print(corners)'''

    if mx==0 or len(coordinates)!=4:
        print("unable to generate result for img",num)
        return

    #print(coordinates.shape)

    coordinates = reorder(coordinates)

    pts1 = np.float32(coordinates)
    pts2 = np.float32([[0, 0], [c, 0], [0, r], [c, r]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (c, r))

    #out = img[Y+2:Y+H-2, X+2:X+W-2]
    out = imgWarp
    #res = cv2.rectangle(img,(X,Y),(X+W,Y+H),(0,255,0),1)
 
    #cv2.imshow('res', out)

    s = 'result' + str(num) + '.jpg'

    cv2.imwrite(s, out)

    im = Image.open(s)
    im = im.convert('RGB')
    imagelist.append(im) 


if __name__=='__main__':
    
    s = 'img'
    cnt = 10

    while cnt<=17:

        s = 'img' + str(cnt) + '.jpg'
        img = cv2.imread(s)
        findPage(img, cnt)
        cnt = cnt+1

    im.save('aditya.pdf', save_all=True, append_images=imagelist)