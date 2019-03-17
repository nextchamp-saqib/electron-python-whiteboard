import cv2
import time
from collections import deque
from imutils.video import VideoStream
import numpy as np
import pyautogui
from pynput.mouse import Button, Controller

mouse = Controller()

from perspective import four_point_transform

trackedPts = deque(maxlen=64)
counter = 0
(dX, dY) = (0, 0)
prevClick = None


def checkForIR(frame):
    frame = cv2.resize(frame, (640, 360))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_range = np.array([160, 100, 70], dtype=np.uint8)
    upper_range = np.array([180, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_range, upper_range)
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)

    lower, contours, upper = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    canvas = np.zeros(frame.shape)
    global mouse, prevClick
    if len(contours) > 0:
        blob = max(contours, key=lambda el: cv2.contourArea(el))
        ((x, y), r) = cv2.minEnclosingCircle(blob)
        M = cv2.moments(blob)
        if M["m00"] > 0:
            center = [int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])]
            cv2.circle(canvas, (center[0], center[1]), 4, (255, 255, 255), -1)
        else:
            center = [int(x), int(y)]

        if r > 1:
            # cv2.circle(canvas, (center[0], center[1]), 4, (0, 255, 255), -1)
            # cv2.imwrite(
            #     "/Users/saqibansari/Documents/WhiteBoard/src/python/canvas.jpg",
            #     canvas,
            # )
            # cv2.imwrite(
            #     "/Users/saqibansari/Documents/WhiteBoard/src/python/frame.jpg",
            #     frame,
            # )
            moveAndClick(center[0], center[1])
    else:
        moveAndClick(0, 0)
    # cv2.imshow("frame", frame)
    # cv2.moveWindow("frame", 0, 0)
    # cv2.imshow("Masked", canvas)
    # cv2.moveWindow("Masked", 640, 10)


def checkXandYrange(x, y):
    if prevClick is not None:
        if abs(prevClick[0] - x) > 1 or abs(prevClick[1] - y) > 1:
            return True
        else:
            return False
    else:
        return False


# def moveAndClick(x, y):
#     click = checkXandYrange(x, y)
#     global prevClick
#     # if click and prevClick is not None:
#     if click and prevClick is not None:
#         relX = x - prevClick[0]
#         relY = y - prevClick[1]
#         pyautogui.dragRel(int(relX * 2), int(relY * 2))
#         # pyautogui.moveTo(int(x * 2), int(y * 2.22))
#         # pyautogui.click(int(x * 2), int(y * 2.22))
#         prevClick = (x, y)
#         return
#     else:
#         # pyautogui.moveTo(int(x * 2), int(y * 2.22))
#         pyautogui.click(int(x * 2), int(y * 2))
#         prevClick = (x, y)
#         return


def moveAndClick(x, y):
    global prevClick, mouse

    if x is 0 and y is 0:
        if prevClick is not None:
            prevClick = None
            mouse.release(Button.left)
        return
    else:
        click = checkXandYrange(x, y)
        if click and prevClick is not None:
            relX = x - prevClick[0]
            relY = y - prevClick[1]
            mouse.move(int(relX * 2), int(relY * 2.19))
            prevClick = (x, y)
        else:
            mouse.position = (int(x * 2), int(y * 2.19))
            while mouse.position != (int(x * 2), int(y * 2.19)):
                pass
            mouse.press(Button.left)
            prevClick = (x, y)


def addToQueue(item):
    global trackedPts
    if item is None:
        trackedPts.appendleft(item)
        return
    if item in trackedPts:
        return
    else:
        trackedPts.appendleft(item)
        return


def Start(coordinates, ip):
    # cap = VideoStream("http://" + str(ip) + ":8080/mjpeg").start()
    cap = cv2.VideoCapture("/Users/saqibansari/Downloads/laser.mp4")
    time.sleep(0.5)

    # while True:
    while cap.isOpened():
        # frame = cap.read()
        ret, frame = cap.read()
        if frame is None:
            print("None")
            # cap = cv2.VideoCapture("/Users/saqibansari/Downloads/laser.mp4")
            # ret, frame = cap.read()
            break

        frame = cv2.resize(frame, (640, 360))
        wrapedImage = frame

        if coordinates is not None:
            wrapedImage = four_point_transform(frame, coordinates)
            wrapedImage = cv2.resize(wrapedImage, (640, 360))

        checkForIR(wrapedImage)

        if cv2.waitKey(33) == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break


c = [[186, 34], [186, 288], [560, 277], [582, 59]]
Start(c, "sjdkfgh")

