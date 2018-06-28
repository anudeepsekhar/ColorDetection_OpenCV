import cv2 as cv
import numpy as np

def proccess(img):
    im2, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv.contourArea(contour), contour) for contour in contours]
    if not contour_sizes ==  []:
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        if cv.contourArea(biggest_contour) > 400:
            return biggest_contour
    else:
        return None

def findBox(color):
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])

    blue_mask = cv.inRange(hsv, lower_blue, upper_blue)
    yellow_mask = cv.inRange(hsv, lower_yellow, upper_yellow)
    red_mask = cv.inRange(hsv, lower_red, upper_red)

    if color == "Red":
        box = proccess(red_mask)
    elif color == "Blue":
        box = proccess(blue_mask)
    elif color == "Yellow":
        box = proccess(yellow_mask)

    return box
    

def drawBox(box, color):
    x,y,w,h = cv.boundingRect(box)
    font = cv.FONT_HERSHEY_SIMPLEX
    if color == (0,0,255):
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        cv.putText(frame,'Red',(x,y), font, 2,(0,0,255),2,cv.LINE_AA)
    elif color == (255,0,0):
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv.putText(frame,'Blue',(x,y), font, 2,(255,0,0),2,cv.LINE_AA)    
    elif color == (0,255,255):
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        cv.putText(frame,'Yellow',(x,y), font, 2,(0,255,255),2,cv.LINE_AA)
    

cap = cv.VideoCapture(1)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    red_box = findBox("Red")
    blue_box = findBox("Blue")
    yellow_box = findBox("Yellow")

    boxes = [[red_box,(0,0,255)],[yellow_box,(0,255,255)],[blue_box,(255,0,0)]]
    # print(boxes)
    for box,color in boxes:
        if box != []:
            drawBox(box,color)
            
    cv.imshow('frame',frame)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()



    

   
       
    

