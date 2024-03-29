import cv2
import numpy as np
from gpiozero import Robot
#from time import sleep

c = 80
cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)

robot = Robot(left=(17, 18), right=(27, 22))
forward_speed = 0.3
turn_speed = 0.5

while True:
    ret, frame = cap.read()
    low_b = np.uint8([5,5,5])
    high_b = np.uint8([0,0,0])
    mask = cv2.inRange(frame, high_b, low_b)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0 :
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print("CX : "+str(cx)+"  CY : "+str(cy))
            if cx >= 110 :
                robot.left(turn_speed)
                '''sleep(0.2)
                robot.forward(forward_speed)'''
                print("Turn Left")
            if cx < 110 and cx > 50 :
                robot.forward(forward_speed)
                print("On Track!")
            if cx <=50 :
                robot.right(turn_speed)
                '''sleep(0.2)
                robot.forward(forward_speed)'''
                print("Turn Right")
            cv2.circle(frame, (cx,cy), 20, (255,255,255), -1)
    else :
        robot.stop()
        print("I don't see the line")
    cv2.drawContours(frame, c, -1, (0,255,0), 1)
    cv2.imshow("Mask",mask)
    cv2.imshow("Frame",frame)
    if cv2.waitKey(1) & 0xff == ord('q'):   # 1 is the time in ms
        robot.stop()
        break
cap.release()
cv2.destroyAllWindows()