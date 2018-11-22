import threading
import time

from PIL import ImageGrab
import numpy as np
import cv2


class record(threading.Thread):

    def __init__(self, fileName):
        threading.Thread.__init__(self)
        self.isStop = False
        screen = ImageGrab.grab()  # 获得当前屏幕
        a, b = screen.size  # 获得当前屏幕的大小
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 编码格式
        self.video = cv2.VideoWriter(fileName, fourcc, 25, (a, b))  # 输出文件命名为test.mp4,帧率为16，可以自己设置
        self.k = np.zeros([200, 200], np.uint8)

    def run(self):
        print("start ===>> " + threading.current_thread().name)
        while True:
            im = ImageGrab.grab()
            imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
            cv2.imshow('imm', self.k)
            self.video.write(imm)
            if cv2.waitKey(1) == ord('q') or self.isStop:
                break
            print("loop ===>> " + threading.current_thread().name)

        self.video.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.isStop = True


if __name__ == '__main__':
    record = record('test.avi')
    print("main===>> " + threading.current_thread().name)
    record.start()
    time.sleep(6)
    record.stop()
    print("main===>> " + threading.current_thread().name)
