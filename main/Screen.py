import pyautogui
import time


def findImage():
    print("findImage....")


def getPosition(image, function=findImage):
    return pyautogui.center(getLocateOnScreen(image, function))


def getLocateOnScreen(image, function=findImage):
    screen = pyautogui.locateOnScreen(image)
    if not screen is None:
        return screen
    else:
        time.sleep(1)
        pyautogui.moveRel(20, 20)
        if not function == None:
            function()
        print(image)
        return getLocateOnScreen(image, function)


if __name__ == '__main__':
    print(getLocateOnScreen(r'/Users/deemons/PycharmProjects/ScrennRecording/main/image/xunhuan.png'))
    print(getPosition(r'/Users/deemons/PycharmProjects/ScrennRecording/main/image/xunhuan.png'))
