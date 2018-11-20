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
        pass
        #     视频停止播放
        self.stop()
        getPosition("./boxue_img/player_player.png")

        #     找视频的名称
        fileName = self.getFileName()

        #     查找视频时长
        during = self.getDuring() - 2

        #     全屏
        # pyautogui.click(getPosition("./boxue_img/full_player.png"))
        # pyautogui.moveTo(500, 500)

        #     播放及录制
        x, y = getPosition("./boxue_img/play_player.png")
        pyautogui.hotkey("ctrl", "f4")
        time.sleep(1)
        pyautogui.click(x, y)

        #     休眠
        time.sleep(during)
        #     检测停止播放图标
        getPosition("./boxue_img/finish.png")
        #     停止录屏，及保存
        pyautogui.hotkey("ctrl", "f2")
        time.sleep(0.5)
        pyperclip.copy(fileName)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        pyautogui.press("enter")



        #   隐藏界面
        self.hideWindow()

        #     重复以上动作
        self.doSingleTask()

    def stop(self):
        pyautogui.click(getPosition("./boxue_img/stop_player.png"))
        pyautogui.moveRel(200, -400)

    def getDuring(self):
        timeInfo = ImageUtils.ocr(
            image_to_bytes(screenshotByImage("./boxue_img/play_player.png", 0, 0, 100, 26)))
        during = timeUtils.handleOcrTime(timeInfo['words_result'][0]['words'].split('/'))
        print(during)
        return during

    def getFileName(self):
        timeInfo = ImageUtils.ocr(
            image_to_bytes(screenshotByImage("./boxue_img/file_name.png", 0, 0, 200, 25)))
        fileName = timeInfo['words_result'][0]['words']
        print(fileName)
        return fileName

    def hideWindow(self):
        position = getPosition("./image/mini_recording.png")
        pyautogui.click(position)
        pyautogui.moveRel(160, None)


if __name__ == '__main__':
    control = Control()
    control.doSingleTask()
    #
    # timeInfo = '00:0126:35'
    # print(timeUtils.handleOcrTime(timeInfo))
