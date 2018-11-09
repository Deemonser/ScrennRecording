import pyautogui
import time


def getPosition(image):
    try:
        return pyautogui.center(pyautogui.locateOnScreen(image))
    except TypeError:
        time.sleep(0.01)
        return getPosition(image)
