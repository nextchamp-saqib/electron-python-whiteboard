import cv2
import numpy as np
import os
import time
from perspective import four_point_transform


def Calibration(ip):
    largestArea = 1000
    finalContour = []
    contourImg = np.zeros((360, 640, 3))
    prevContourImg = contourImg
    delay = 20
    end_time = time.time() + delay
    coordinates = []

    cap = cv2.VideoCapture("http://" + str(ip) + ":8080/mjpeg")
    # cap = cv2.VideoCapture("http://192.168.2.104:8080/mjpeg")

    # cap = cv2.VideoCapture("/Users/saqibansari/Downloads/calibration.mp4")
    time.sleep(1.0)

    ret, prevFrame = cap.read()

    while cap.isOpened():
        ret, frame = cap.read()

        if frame is None:
            print(coordinates)
            cap.release()
            cv2.destroyAllWindows()
            # for i in range(1, 5):
            cv2.waitKey(1)
            return coordinates, prevFrame
            break

        prevFrame = cv2.resize(prevFrame, (640, 360))
        frame = cv2.resize(frame, (640, 360))
        prevGrayFrame = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)  # Greying
        currentGrayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Greying

        diff = cv2.absdiff(
            prevGrayFrame, currentGrayFrame
        )  # Difference in prev frame and current frame
        ret, threshold = cv2.threshold(
            diff, 20, 255, cv2.THRESH_BINARY
        )  # Thresholding the difference frame

        blurred = cv2.GaussianBlur(
            threshold, (7, 7), 0
        )  # Blurring the thresholded image to get smooth frame
        ret, final_threshold = cv2.threshold(
            blurred, 35, 255, cv2.THRESH_BINARY
        )  # Again Thresholding
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(
            final_threshold, kernel, iterations=1
        )  # Dilation and erosion removes small noise
        eroded = cv2.erode(dilated, kernel, iterations=1)
        # cv2.imshow("TAB 1", frame)
        # cv2.imshow("TAB 2", eroded)
        # cv2.moveWindow("TAB 2", 0, 10)

        # Here we find the objects which are moving i.e different from 2 frames in our case rectangle is moving.
        m, contours, hierarchy = cv2.findContours(
            eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        # if we find a moving rectangle
        if len(contours) > 0:
            for c in contours:
                area = cv2.contourArea(c)
                # finding the rectangle with largest area
                if area > largestArea and area < 92000:
                    largestArea = area
                    contourImg = np.zeros((360, 640, 3))
                    # Draw the rectangle
                    cv2.drawContours(contourImg, [c], 0, (255, 255, 255), 2)
                    # cv2.imshow("TAB 3", contourImg)
                    # cv2.moveWindow("TAB 3", 640, 10)
                    prevContourImg = contourImg
                    finalContour = c

        if prevContourImg is not contourImg:
            end_time = time.time() + delay

        # if contourimage is unchanged for 15 secs then that is the final largest rectangle which is the screen
        if time.time() > end_time:
            epsilon = 0.07 * cv2.arcLength(finalContour, True)
            approx = cv2.approxPolyDP(finalContour, epsilon, True)
            for pts in approx:
                coordinates.append([int(pts[0][0]), int(pts[0][1])])
                cv2.circle(frame, (int(pts[0][0]), int(pts[0][1])), 2, (0, 0, 255), -1)

            vrx = np.array(coordinates, np.int32)
            vrx = vrx.reshape((-1, 1, 2))
            liveImage = cv2.polylines(frame, [vrx], True, (0, 0, 255), 3)

            cv2.imwrite(
                "/Users/saqibansari/Documents/WhiteBoard/src/python/liveImage.jpg",
                liveImage,
            )

            wrapedImage = frame
            wrapedImage = four_point_transform(frame, coordinates)

            cv2.imwrite(
                "/Users/saqibansari/Documents/WhiteBoard/src/python/wrapedImage.jpg",
                wrapedImage,
            )
            # prevImg = np.zeros((360,640,3))
            # cv2.drawContours(prevImg,[approx], 0, (255,255,255), 2)
            # cv2.imshow("final", prevImg)
            # cv2.moveWindow("final", 0, 320)
            print(coordinates)
            cap.release()
            cv2.destroyAllWindows()
            # for i in range(1, 5):
            cv2.waitKey(1)
            return coordinates, frame
            break

        prevFrame = frame

        if cv2.waitKey(33) == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)


# Calibration("283746")
