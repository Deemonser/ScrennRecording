import threading
import time

from PIL import ImageGrab
import numpy as np
import cv2
import multiprocessing


class filter():

    def __init__(self, filePath):
        # multiprocessing.Process.__init__(self)
        self.video = cv2.VideoCapture(filePath)
        self.target = cv2.cvtColor(cv2.imread("test.png"), cv2.COLOR_BGR2GRAY)
        self.out = cv2.VideoWriter('test_copy.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (1920, 1080))
        self.th, self.tw = self.target.shape[:2]

    def run(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(gray, self.target, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            br = (min_loc[0] + self.tw, min_loc[1] + self.th)
            cv2.rectangle(frame, min_loc, br, (0, 0, 255), 2)
            cv2.putText(frame, "i love you", (min_loc[0], min_loc[1] + self.th), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                        (179, 93, 46), 2)
            cv2.imshow("", frame)
            self.out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video.release()
        self.out.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    record = filter('test.avi')
    record.run()
    # record.join()
    print("main===>> " + threading.current_thread().name)
    # cv2.imshow("", cv2.imread("test.png"))
    # cv2.waitKey(0)
