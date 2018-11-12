import pyautogui
import time


def getPosition(image):
    return pyautogui.center(getLocateOnScreen(image))


def getLocateOnScreen(image):
    screen = pyautogui.locateOnScreen(image)
    if not screen is None:
        return screen
    else:
        time.sleep(0.1)
        pyautogui.moveRel(10, 10)
        return getLocateOnScreen(image)


if __name__ == '__main__':
    print(getLocateOnScreen(r'/Users/deemons/PycharmProjects/ScrennRecording/main/image/xunhuan.png'))
    print(getPosition(r'/Users/deemons/PycharmProjects/ScrennRecording/main/image/xunhuan.png'))
