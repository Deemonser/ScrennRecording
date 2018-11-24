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

        self.target = img2HSV(cv2.imread("test2.png", cv2.IMREAD_UNCHANGED))
        size = (int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print(size)
        self.out = cv2.VideoWriter('test_copy.avi', cv2.VideoWriter_fourcc(*'XVID'), self.video.get(cv2.CAP_PROP_FPS),
                                   size)
        self.th, self.tw = self.target.shape[:2]

    def run(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            mask = img2HSV(frame)

            # cv2.imshow("mask", mask)

            result = cv2.matchTemplate(mask, self.target, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            ok = max_loc

            br = (ok[0] + self.tw, ok[1] + self.th)
            cv2.rectangle(frame, ok, br, (255, 255, 255), thickness=cv2.FILLED)
            cv2.putText(frame, "i love you", (ok[0], ok[1] + self.th), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                        (179, 93, 46), 2)
            cv2.imshow("", frame)
            self.out.write(frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        self.video.release()
        self.out.release()
        cv2.destroyAllWindows()


def img2HSV(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 90, 60])  # 所要检测的像素范围
    upper = np.array([11, 260, 260])  # 此处检测绿色区域
    mask = cv2.inRange(hsv, lowerb=lower, upperb=upper)
    return mask


def getpos(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(HSV[y, x])


mat = cv2.imread("test2.png", cv2.IMREAD_UNCHANGED)
# cv2.imshow("", mat)

HSV = cv2.cvtColor(mat, cv2.COLOR_BGR2HSV)


def getHSV():
    # th2=cv2.adaptiveThreshold(imagegray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    cv2.imshow("imageHSV", HSV)
    cv2.imshow('image', mat)
    cv2.setMouseCallback("imageHSV", getpos)
    cv2.waitKey(0)


# [  2 250 248]
# [  3 247 255]
# [  3 255 255]
# [  3 255 254]
# [  3 255 255]
# [  3 255 180]
# [  4 238 133]
# [ 11 140  62]
# [ 2 98 68]
# [  3 131  70]
# [  1 153 100]
# [  0   0 255]
# [  0   0 255]
# [  2 184 140]

if __name__ == '__main__':
    record = filter('01-PS and AI.mp4')
    record.run()
    record.join()
    # print("main===>> " + threading.current_thread().name)

    # hsv = cv2.cvtColor(cv2.imread("test2.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2HSV)
    # lower = np.array([0, 130, 60])  # 所要检测的像素范围
    # upper = np.array([11, 260, 260])  # 此处检测颜色区域
    # mask = cv2.inRange(hsv, lowerb=lower, upperb=upper)
    # cv2.imshow("mask", mask)

    # getHSV()

    # cv2.imshow("", img2HSV(cv2.imread("test2.png", cv2.IMREAD_UNCHANGED)))

    # cv2.waitKey(0)
