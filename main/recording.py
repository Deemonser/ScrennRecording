import time, os
# https://www.jianshu.com/p/552f96aa85dc

import pyautogui
import pyperclip
from main import Screen


class Record:

    def __init__(self, filePath, during):
        self.path = os.path.join(os.path.dirname(os.path.dirname(filePath)), "视频录制")
        srcName = os.path.split(filePath)[1]
        self.fileName = srcName.replace(os.path.splitext(srcName)[1], ".mp4")
        self.during = during

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            self.changePath()

    def startRecord(self):
        pyautogui.hotkey("ctrl", "f1")

    def stopRecord(self):
        pyautogui.hotkey("ctrl", "f2")
        time.sleep(1)
        pyperclip.copy(self.fileName)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.press("enter")

    def hideWindow(self):
        pyautogui.click(Screen.getPosition("./image/mini_recording.png"))

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
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.keyUp("shift")
        time.sleep(3)
        pyautogui.press("enter")
        time.sleep(0.5)
        x1, y1 = Screen.getPosition("./image/close_record_setting.png")
        pyautogui.click(x1 + 20, y1)
        time.sleep(0.5)
        pyautogui.click(Screen.getPosition("./image/mini_recording.png"))
