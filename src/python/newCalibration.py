import cv2
import numpy as np
import os
import time


def Calibration():
    largestArea = 1000
    finalContour = []
    contourImg = np.zeros((360, 640, 3))
    prevContourImg = contourImg
    delay = 20
    end_time = time.time() + delay
    coordinates = []

    # cap = cv2.VideoCapture("http://192.168.43.36:8258/video")
    cap = cv2.VideoCapture(
        "/Users/saqibansari/Documents/WhiteBoard/src/python/calibration7.mp4"
    )
    time.sleep(1.0)

    ret, prevFrame = cap.read()

    while cap.isOpened():
        ret, frame = cap.read()

        if frame is None:
            print("ended")
            # ret, frame = cap.read()
            return coordinates, frame
            break

        prevFrame = cv2.resize(prevFrame, (640, 360))
        frame = cv2.resize(frame, (640, 360))
        prevGrayFrame = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)
        currentGrayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(prevGrayFrame, currentGrayFrame)
        ret, threshold = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
        
        blurred = cv2.GaussianBlur(threshold, (7, 7), 0)
        ret, final_threshold = cv2.threshold(blurred, 35, 255, cv2.THRESH_BINARY)
        kernel = np.ones((5,5), np.uint8)
        dilated = cv2.dilate(final_threshold, kernel, iterations = 1)
        eroded = cv2.erode(dilated, kernel, iterations = 1)
        # cv2.imshow('TAB 2', eroded)

        m, contours, hierarchy = cv2.findContours(
            eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        if len(contours) > 0:
            for c in contours:
                area = cv2.contourArea(c)
                if area > largestArea and area < 90000:
                    largestArea = area
                    contourImg = np.zeros((360, 640, 3))
                    cv2.drawContours(contourImg, [c], 0, (255, 255, 255), 2)
                    cv2.imshow("TAB 3", contourImg)
                    cv2.moveWindow("TAB 3", 0, 520)
                    prevContourImg = contourImg
                    finalContour = c

        if prevContourImg is not contourImg:
            end_time = time.time() + delay

        if time.time() > end_time:
            epsilon = 0.07 * cv2.arcLength(finalContour, True)
            approx = cv2.approxPolyDP(finalContour, epsilon, True)
            for pts in approx:
                coordinates.append([int(pts[0][0]), int(pts[0][1])])
                cv2.circle(frame, (int(pts[0][0]), int(pts[0][1])), 2, (0,0,255), -1)
            
            # x = 4
            # y = 2
            # coordinates[0][0] -= x
            # coordinates[0][1] -= y

            # coordinates[1][0] -= x
            # coordinates[1][1] += y

            # coordinates[2][0] += x
            # coordinates[2][1] += y

            # coordinates[3][0] += x
            # coordinates[3][1] -= y

            vrx = np.array(coordinates, np.int32)
            vrx = vrx.reshape((-1,1,2))
            # liveImage = np.zeros((360,640,3))
            liveImage = cv2.polylines(frame, [vrx], True, (0,0,255),3)
            cv2.imwrite("/Users/saqibansari/Documents/WhiteBoard/src/python/liveImage.jpg", liveImage)

            # cv2.imwrite("/Users/saqibansari/Documents/WhiteBoard/src/python/liveImage.jpg", frame)

            # prevImg = np.zeros((360,640,3))
            # cv2.drawContours(prevImg,[approx], 0, (255,255,255), 2)
            # cv2.imshow("final", prevImg)
            # cv2.moveWindow("final", 0, 320)

            cap.release()
            cv2.destroyAllWindows()
            for i in range(1, 5):
                cv2.waitKey(1)
            return coordinates, frame
            break

        prevFrame = frame

        if cv2.waitKey(33) == ord("q"):
            cap.release()
            break


# Calibration()