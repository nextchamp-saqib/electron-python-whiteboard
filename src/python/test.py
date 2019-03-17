import time

# import pyautogui
from pynput.mouse import Button, Controller

mouse = Controller()
c = 0

time.sleep(1.0)
mouse.position = (640, 360)
mouse.press(Button.left)
while True:
    mouse.move(6, 6)
    mouse.move(6, -6)
    c += 1
    if c > 20:
        break

mouse.release(Button.left)
# print(time.time() - start)

