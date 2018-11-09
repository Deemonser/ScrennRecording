from main.Video import Movie_MP4
from main.FileUtils import getFile
from main.recording import Record
import os
import time


class Control:

    def __init__(self, path, endName, rate, delay=0.0):
        self.path = path
        self.endName = endName
        self.rate = rate
        self.delay = delay

    def doAllTask(self):
        files = getFile(self.path, self.endName)
        print(files)
        for file in files:
            self.doSingleTask(file)

    def doSingleTask(self, file):
        movie = Movie_MP4(file)
        print(str(movie.getSize()))

        during = movie.getDuringByRate(self.rate)
        print(str(during))

        record = Record(file, during)
        # 播放
        movie.play()
        movie.fullWindow()
        # 延时录屏
        time.sleep(self.delay)
        # 开启录屏
        record.startRecord()
        # 录屏中，等待
        time.sleep(during)
        # 停止录屏
        record.stopRecord()
        record.hideWindow()
        # 关闭播放窗口
        movie.closeWindow()
        time.sleep(2)


if __name__ == '__main__':
    rate = 1000000 / 1
    control = Control(r'E:\pythonProject\Test', '.itcast', rate)
    control.doAllTask()
