from imutils.video import FileVideoStream
from imutils.video import FPS
import imutils
import cv2
import time

# fvs = FileVideoStream('http://192.168.2.106:8258/video').start()
# time.sleep(1.0)

# while fvs.more():
#   frame = fvs.read()
#   frame = imutils.resize(frame, width=640)
#   cv2.imshow('video', frame)

#   if cv2.waitKey(33) == ord('q'):
#     fvs.stop()
#     break


cap = cv2.VideoCapture('http://192.168.2.106:8258/video')
time.sleep(1.0)

while cap.isOpened():
  ret, frame = cap.read()
  frame = imutils.resize(frame, width=640)
  cv2.imshow('video', frame)

  if cv2.waitKey(33) == ord('q'):
    cap.release()
    break
