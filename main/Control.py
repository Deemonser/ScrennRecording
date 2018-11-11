from main import timeUtils
from main.Video import Movie_MP4
from main.FileUtils import getFile
from main.recording import Record
import os
import time


class Control:

    def __init__(self, path, endName, delay=0.0):
        self.path = path
        self.endName = endName

        self.delay = delay

    def doAllTask(self):
        files = getFile(self.path, self.endName)
        print(files)
        for file in files:
            self.doSingleTask(file)

    def doSingleTask(self, file):
        record = Record(file)
        if record.isExit():
            return

        movie = Movie_MP4(file)
        print("size=%s" % str(movie.getSize()))
        # 播放
        movie.play()
        movie.fullWindow()
        during = movie.getDuring()
        print("during=%s" % (str(during)))
        movie.prepare()

        record.prepare(during)
        # 开启录屏
        record.startRecord()
        # 延时录屏
        time.sleep(self.delay)
        movie.start()
        # 录屏中，等待
        time.sleep(during)
        # 停止录屏
        record.stopRecord()
        record.hideWindow()
        # 关闭播放窗口
        movie.closeWindow()
        time.sleep(5)


if __name__ == '__main__':
    control = Control(r'F:\UI设计-基础班\【第1天】Photoshop基础\1-视频', '.itcast', 1.0)
    control.doAllTask()
    #
    # timeInfo = '00:0126:35'
    # print(timeUtils.handleOcrTime(timeInfo))
