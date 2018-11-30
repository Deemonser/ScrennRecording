import time, os
# https://www.jianshu.com/p/552f96aa85dc

import pyautogui
import pyperclip
import Locate


class Record:

    def __init__(self, filePath):
        self.path = os.path.join(os.path.dirname(os.path.dirname(filePath)), "视频录制")
        srcName = os.path.split(filePath)[1]
        self.fileName = srcName.replace(os.path.splitext(srcName)[1], ".mp4")

    def prepare(self, during):
        self.during = during

        self.lunch()
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
        time.sleep(1)
        pyperclip.copy(self.fileName)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)
        pyautogui.press("enter")
        print("stopRecord")

    def lunch(self):
        os.startfile('./EVCapture')
        time.sleep(1)
        pyautogui.hotkey("ctrl", "f3")
        time.sleep(0.5)

    def hideWindow(self):
        position = Locate.getPosition("./img/recorder_mini.png", self.lunch)
        pyautogui.click(position)
        pyautogui.moveRel(160, None)

    def changePath(self):
        pyautogui.click(Locate.getPosition("./img/recorder_setting.png", self.lunch))
        x, y = Locate.getPosition("./img/recorder_setting_with_text.png")
        pyautogui.click(x, y + 36)
        pyautogui.click(Locate.getPosition("./img/recorder_setting_change.png"))
        time.sleep(0.5)
        pyautogui.click(Locate.getPosition("./img/recorder_choose_path.png"))
        time.sleep(0.5)
        pyperclip.copy(self.path)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        pyautogui.press("enter")
        pyautogui.keyDown("shift")
        pyautogui.press("tab", 5)
        pyautogui.keyUp("shift")
        pyautogui.press("enter")
        x1, y1 = Locate.getPosition("./img/recorder_close_setting.png")
        pyautogui.click(x1 + 20, y1)
        pyautogui.click(Locate.getPosition("./img/recorder_mini.png"))
