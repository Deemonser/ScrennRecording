import time, os
# https://www.jianshu.com/p/552f96aa85dc

import pyautogui
import pyperclip
from main import Screen


class Record:

    def __init__(self, filePath):
        self.path = os.path.join(os.path.dirname(os.path.dirname(filePath)), "视频录制")
        srcName = os.path.split(filePath)[1]
        self.fileName = srcName.replace(os.path.splitext(srcName)[1], ".mp4")

    def prepare(self, during):
        self.during = during

        os.startfile(r'C:\Program Files (x86)\EVCapture\EVCapture.exe')
        time.sleep(1)
        pyautogui.hotkey("ctrl", "f3")
        self.hideWindow()

        print("record save path: %s" % (self.path))
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.changePath()

    def isExit(self):
        return os.path.exists(os.path.join(self.path, self.fileName))

    def startRecord(self):
        pyautogui.hotkey("ctrl", "f1")
        print('startRecord')

    def stopRecord(self):
        pyautogui.hotkey("ctrl", "f2")
        time.sleep(2)
        pyperclip.copy(self.fileName)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.press("enter")
        print("stopRecord")

    def hideWindow(self):
        position = Screen.getPosition("./image/mini_recording.png")
        pyautogui.click(position)
        pyautogui.moveRel(-20, None)

    def changePath(self):
        pyautogui.hotkey("ctrl", "f3")
        pyautogui.click(Screen.getPosition("./image/record_setting.png"))
        x, y = Screen.getPosition("./image/record_setting_normal.png")
        pyautogui.click(x, y + 36)
        pyautogui.click(Screen.getPosition("./image/record_setting_change.png"))
        time.sleep(0.5)
        pyautogui.click(Screen.getPosition("./image/choose_path.png"))
        time.sleep(0.5)
        pyperclip.copy(self.path)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        pyautogui.press("enter")
        pyautogui.keyDown("shift")
        pyautogui.press("tab", 5)
        pyautogui.keyUp("shift")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)
        x1, y1 = Screen.getPosition("./image/close_record_setting.png")
        pyautogui.click(x1 + 20, y1)
        time.sleep(0.5)
        pyautogui.click(Screen.getPosition("./image/mini_recording.png"))
