import time, os
# https://www.jianshu.com/p/552f96aa85dc

import pyautogui


class Record:

    def __init__(self, path, during):
        self.path = str(path).replace(str(os.path.splitext(path)[1]), ".mp4")
        self.during = during

    def startRecord(self):
        pyautogui.hotkey("ctrl", "f1")

    def stopRecord(self):
        pyautogui.hotkey("ctrl", "f2")
        time.sleep(1)
        pyautogui.typewrite(self.path)
        pyautogui.press("enter")

    def hideWindow(self):
        pyautogui.hotkey("hide Record Window!")
