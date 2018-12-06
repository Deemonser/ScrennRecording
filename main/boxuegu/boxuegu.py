import os
import sys

import pyperclip
import pyautogui
from Screen import getPosition
import timeUtils, ImageUtils
import time


class Control:

    def doSingleTask(self):
        self.i = 0
        #     视频停止播放
        self.stop()
        x, y = getPosition("./boxue_img/play_player.png", self.stop)
        pyautogui.press("left", 6, interval=0.1)

        #     找视频的名称
        fileName = self.getFatherName() + "_" + self.getChildName() + "_" + self.getFileName()
        print(fileName)
        pyperclip.copy(fileName)
        pyautogui.moveTo(x, y)

        #     查找视频时长
        during = self.getDuring() - 1
        #     全屏
        # pyautogui.click(getPosition("./boxue_img/full_player.png"))
        # pyautogui.moveTo(500, 500)

        # os.startfile(r'C:\Program Files (x86)\EVCapture\EVCapture.exe')
        pyautogui.click(563, 1065, duration=0.2)
        time.sleep(1)
        pyautogui.hotkey("ctrl", "f3")
        time.sleep(0.5)
        self.hideWindow()

        #     播放及录制
        pyautogui.hotkey("ctrl", "f4", during=0.2)
        time.sleep(1)
        pyautogui.click(x, y, duration=0.2)
        time.sleep(0.5)
        pyautogui.moveRel(None, -500)

        #     休眠
        time.sleep(during)
        #     检测停止播放图标
        # pyautogui.moveTo(x, y)
        # getPosition("./boxue_img/player_end.png")

        #     停止录屏，及保存
        pyautogui.hotkey("ctrl", "f2", during=0.2)
        time.sleep(1)
        pyautogui.hotkey("ctrl", "v", during=0.2)
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(1)

        #   隐藏界面
        self.hideWindow()

        #     重复以上动作
        self.doSingleTask()

    def find_next(self):
        self.i = self.i + 1
        print("find count:" + str(self.i))
        if self.i % 30 == 0:
            print("find image: play_player")
            result = pyautogui.locateOnScreen("./boxue_img/play_player.png")
            if not result is None:
                pyautogui.click(pyautogui.center(result), duration=0.2)
                self.i = 0

        if self.i % 10 == 0:
            print("find image: next")
            result = pyautogui.locateOnScreen("./boxue_img/next.png")
            if not result is None:
                pyautogui.click(pyautogui.center(result), duration=0.2)
                self.i = 0

    def stop(self):
        position = getPosition("./boxue_img/stop_player.png", self.find_next)
        time.sleep(0.5)
        pyautogui.click(position, duration=0.2)
        print("click stop")
        pyautogui.moveRel(None, -300)

    def getDuring(self):
        print("getDuring")
        timeInfo = ImageUtils.ocr(
            ImageUtils.image_to_bytes(ImageUtils.screenshotByImage("./boxue_img/play_player.png", 60, 0, 45, 26)))
        during = timeUtils.t2s(timeInfo['words_result'][0]['words'])
        print(during)
        return during

    def getFileName(self):
        x, y = getPosition("./boxue_img/file_name.png")
        pyautogui.mouseDown(x, y)
        pyautogui.moveRel(215, None)
        pyautogui.hotkey("ctrl", "c")
        pyautogui.moveRel(50, None)
        pyautogui.mouseUp()
        pyautogui.click(1800, 885)
        fileName = pyperclip.paste()
        print(fileName)
        return fileName

    def getChildName(self):
        x, y = getPosition("./boxue_img/child_name.png")
        pyautogui.mouseDown(x - 250, y)
        pyautogui.moveRel(260, None)
        pyautogui.hotkey("ctrl", "c")
        pyautogui.moveRel(40, None)
        pyautogui.mouseUp()
        pyautogui.click(1800, 885)
        childName = pyperclip.paste()
        print(childName)
        return childName

    def getFatherName(self):
        x, y = getPosition("./boxue_img/father_name.png")
        pyautogui.mouseDown(x - 30, y + 50)
        pyautogui.moveRel(270, None)
        pyautogui.hotkey("ctrl", "c")
        pyautogui.mouseUp()
        fatherName = pyperclip.paste()
        print(fatherName)
        return fatherName

    def hideWindow(self):
        position = getPosition("./boxue_img/small.png")
        pyautogui.click(position)
        pyautogui.moveRel(160, None)


if __name__ == '__main__':
    try:
        Control().doSingleTask()
    except:
        print("Unexpected error:", sys.exc_info())  # sys.exc_info()返回出错信息

    os.system("pause")
