# import the necessary packages
import numpy as np
import cv2
import os
# import pyautogui

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = np.sum(pts, axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # warped = cv2.resize(wraped, (maxWidth+maxWidth, maxHeight))

    # return the warped image
    return warped


origCordinates = []


def mouseClickHandler(event, x, y, flags, params):
    global image, wrapedImage
    if event == cv2.EVENT_LBUTTONDOWN:
        origCordinates.append((x, y))
        print(origCordinates)

    if len(origCordinates) == 4:
        wrapedImg = four_point_transform(frame, origCordinates)
        # show the original and warped images
        cv2.namedWindow("Wraped")
        cv2.imshow("Wraped", cv2.resize(wrapedImg, (1280, 720)))
        # print(wrapedImage.shape)
        # cv2.setMouseCallback('Wraped', mouseClickHandlerWraped)


# def mouseClickHandlerWraped(event, x, y, flag, params):
#   if event == cv2.EVENT_LBUTTONDOWN:
#     X = x/wrapedImage.shape[1]
#     Y = y/wrapedImage.shape[0]
#     print(X, Y)
#     screen_x = int(X*1279)
#     screen_y = int(Y*799)
#     pyautogui.moveTo(screen_x, screen_y, 0.1)


def correct(coordinates):
    # cap = cv2.VideoCapture("http://192.168.43.36:8258/video")
    cap = cv2.VideoCapture(
        "/Users/saqibansari/Documents/WhiteBoard/src/python/calibration7.mp4"
    )
    print(coordinates)

    while cap.isOpened():
        ret, frame = cap.read()

        if frame is None:
            cv2.destroyAllWindows()
            for i in range(1, 5):
                cv2.waitKey(1)  # just to destroy all windows
            cap.release()
            return 'no frames'
        
        frame = cv2.resize(frame, (640, 360))
        wrapedImage = frame
        wrapedImage = four_point_transform(frame, coordinates)
        cv2.imshow("wrapedImage", wrapedImage)
        if cv2.waitKey(33) == ord("q"):
            cap.release()
            break

        # cv2.namedWindow('image')
        # cv2.setMouseCallback('image', mouseClickHandler)
        # cv2.imshow('image', cv2.resize(frame, (640, 360)))
        # cv2.imshow('wrapedImage', cv2.resize(wrapedImage, (1280, 720)))
        
        # cv2.waitKey(0)
    return 'Done'

