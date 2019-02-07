import cv2
import time
import imutils

from perspective import order_points, four_point_transform, correct
from newCalibration import Calibration


def Start():
    # cap = cv2.VideoCapture('/Users/saqibansari/Documents/WhiteBoard/src/python/rectCalibration5.mp4')
    coordinates, frame = Calibration()
    print(coordinates)

    # cap = cv2.VideoCapture("http://192.168.2.110:8258/video")

    # while cap.isOpened():
    # ret, frame = cap.read()
    # frame = imutils.resize(frame, width=640)
    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    wraped = four_point_transform(frame, coordinates)
    # wraped = correct()
    cv2.imshow("og", frame)
    cv2.imshow("wraped", wraped)
    cv2.moveWindow("wraped", 0, 640)
    cv2.moveWindow("og", 0, 640)
    # cv2.imshow('main', imutils.resize(wraped, width=640))

    if cv2.waitKey(33) == ord("q"):
        cap.release()
        # break

    time.sleep(1000)


