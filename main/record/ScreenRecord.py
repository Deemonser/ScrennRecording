import threading
import time

from PIL import ImageGrab
import numpy as np
import cv2
import multiprocessing


class record(multiprocessing.Process):

    def __init__(self, fileName, isStart, queue):
        multiprocessing.Process.__init__(self)
        self.isStart = isStart
        self.queue = queue
        screen = ImageGrab.grab()  # 获得当前屏幕
        a, b = screen.size  # 获得当前屏幕的大小
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 编码格式
        self.video = cv2.VideoWriter(fileName, fourcc, 16, (a, b))  # 输出文件命名为test.mp4,帧率为16，可以自己设置
        self.k = np.zeros([200, 200], np.uint8)

    def run(self):
        print("start ===>> " + threading.current_thread().name)
        while True:
            im = ImageGrab.grab()
            imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
            # cv2.imshow('imm', self.k)
            self.queue.put(imm)
            is_stop = self.isStart.value
            print("loop ===>> " + str(is_stop) + time.ctime())
            if cv2.waitKey() == ord('q') or not is_stop:
                break

        while not q.empty():
            self.video.write(q.get())

        self.video.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    q = multiprocessing.Queue()
    isStart = multiprocessing.Value('b', True)
    record = record('test.avi', isStart, q)
    record.start()
    time.sleep(20)
    isStart.value = False
    record.join()
    print("main===>> " + threading.current_thread().name)
