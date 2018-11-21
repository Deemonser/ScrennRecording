from main import timeUtils, ImageUtils
from main.ImageUtils import image_to_bytes, screenshotByImage
from main.Video import Movie_MP4
from main.FileUtils import getFile
from main.recording import Record
from main.Screen import *
import pyperclip
import os
import time


class Control:

    def doSingleTask(self):
        #     视频停止播放
        self.stop()

        x, y = getPosition("./boxue_img/play_player.png")

        #     找视频的名称
        fileName = self.getFileName()

        #     查找视频时长
        during = self.getDuring() - 1
        pyperclip.copy(fileName)
        #     全屏
        # pyautogui.click(getPosition("./boxue_img/full_player.png"))
        # pyautogui.moveTo(500, 500)

        #     播放及录制
        pyautogui.hotkey("ctrl", "f4")
        time.sleep(1)
        pyautogui.click(x, y)
        pyautogui.moveRel(None, -500)

        #     休眠
        time.sleep(during)
        #     检测停止播放图标
        # pyautogui.moveTo(x, y)
        # getPosition("./boxue_img/player_end.png")

        #     停止录屏，及保存
        pyautogui.hotkey("ctrl", "f2")
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)
        pyautogui.press("enter")

        #   隐藏界面
        self.hideWindow()

        #     重复以上动作
        self.doSingleTask()

    def find_next(self):
        if self.i > 10:
            result = pyautogui.locateAllOnScreen('./next.png')
            if not result is None:
                pyautogui.click(pyautogui.center(result))
                self.i = 0

    def stop(self):
        self.i = 0
        pyautogui.click(getPosition("./boxue_img/stop_player.png"), self.find_next())
        print("click stop")
        pyautogui.moveRel(None, -300)

    def getDuring(self):
        print("getDuring")
        timeInfo = ImageUtils.ocr(
            image_to_bytes(screenshotByImage("./boxue_img/play_player.png", 55, 0, 45, 26)))
        during = timeUtils.t2s(timeInfo['words_result'][0]['words'])
        print(during)
        return during

    def getFileName(self):
        print("getFileName")
        timeInfo = ImageUtils.ocr(
            image_to_bytes(screenshotByImage("./boxue_img/file_name.png", 0, 0, 200, 25)))
        fileName = timeInfo['words_result'][0]['words']
        print(fileName)
        return fileName

    def hideWindow(self):
        position = getPosition("./boxue_img/small.png")
        pyautogui.click(position)
        pyautogui.moveRel(160, None)


if __name__ == '__main__':
    control = Control()
    control.doSingleTask()
    #
    # timeInfo = '00:0126:35'
    # print(timeUtils.handleOcrTime(timeInfo))
