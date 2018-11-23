import pyperclip

from main import timeUtils, ImageUtils
from main.ImageUtils import image_to_bytes, screenshotByImage
from main.Screen import *


class Control:

    def doSingleTask(self):
        self.i = 0
        #     视频停止播放
        self.stop()
        x, y = getPosition("./boxue_img/play_player.png")
        pyautogui.press("left", 5, interval=0.1)

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
        time.sleep(0.2)
        pyautogui.press("enter")

        #   隐藏界面
        self.hideWindow()

        #     重复以上动作
        self.doSingleTask()

    def find_next(self):
        self.i = self.i + 1
        if self.i > 10:
            print("find_next")
            result = pyautogui.locateOnScreen("./boxue_img/next.png")
            if not result is None:
                pyautogui.click(pyautogui.center(result), duration=0.2)
                self.i = 0

    def stop(self):
        pyautogui.click(getPosition("./boxue_img/stop_player.png", self.find_next), duration=0.2)
        print("click stop")
        pyautogui.moveRel(None, -300)

    def getDuring(self):
        print("getDuring")
        timeInfo = ImageUtils.ocr(
            image_to_bytes(screenshotByImage("./boxue_img/play_player.png", 60, 0, 45, 26)))
        during = timeUtils.t2s(timeInfo['words_result'][0]['words'])
        print(during)
        return during

    def getFileName(self):
        x, y = getPosition("./boxue_img/file_name.png")
        pyautogui.mouseDown(x, y)
        pyautogui.moveRel(250, None)
        pyautogui.hotkey("ctrl", "c")
        pyautogui.moveRel(20, None)
        pyautogui.mouseUp()
        pyautogui.click(1800, 885)
        fileName = pyperclip.paste()
        print(fileName)
        return fileName

    def getChildName(self):
        x, y = getPosition("./boxue_img/child_name.png")
        pyautogui.mouseDown(x - 260, y)
        pyautogui.moveRel(270, None)
        pyautogui.hotkey("ctrl", "c")
        pyautogui.moveRel(20, None)
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
    control = Control()
    control.doSingleTask()
    #
    # timeInfo = '00:0126:35'
    # print(timeUtils.handleOcrTime(timeInfo))
