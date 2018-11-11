import pyautogui
import time


def getPosition(image):
    screen = pyautogui.locateOnScreen(image)
    if not screen is None:
        return pyautogui.center(screen)
    else:
        time.sleep(0.1)
        pyautogui.moveRel(5,5)
        return getPosition(image)
