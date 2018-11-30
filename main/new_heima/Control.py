from Player import Movie_MP4
from FileUtils import getFile
from recording import Record
import time


class Control:

    def __init__(self, path, endName, delay=0.0):
        self.path = path
        self.endName = endName

        self.delay = delay

    def doAllTask(self):
        files = getFile(self.path, self.endName)
        print("file count: %d" % (files.__len__()))
        print(files)
        i = 0
        for file in files:
            i = i + 1
            print("current file: %d /  %d" % (i, files.__len__()))
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
        during = movie.getDuring() * 0.9942
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
    control = Control(r'F:\UI设计-就业班', '.itcast', 1.0)
    control.doAllTask()
    #
    # timeInfo = '00:0126:35'
    # print(timeUtils.handleOcrTime(timeInfo))
