import cv2
import pyautogui

if __name__ == '__main__':
    while True:
        result = pyautogui.locateOnScreen('test.png')
        if result is None:
            print('None')
        else:
            print(result)
