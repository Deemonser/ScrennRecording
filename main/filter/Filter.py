import os, shutil

import multiprocessing
from multiprocessing.pool import Pool
from pydub import AudioSegment
import subprocess
from main import FileUtils
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import math
import time
import cv2
import pathlib


class filter:

    def __init__(self, filePath, imagetarget):
        self.filePath = filePath
        # 读取 目标图片
        self.target = imagetarget
        # 目标图片的宽高
        self.th, self.tw = self.target.shape[:2]

    def start(self):
        print(time.ctime())
        self.prepare()

        self.coverImage()

        self.handle()

        print(time.ctime())

    def prepare(self):
        # ffmpeg 不识别空格，重命名
        self.videoInfo = VideoInfo(self.filePath)
        # 过滤 logo 后的视频文件名

        os.rename(self.videoInfo.srcPath, self.videoInfo.tmpPath)

        # 创建视频
        self.video = cv2.VideoCapture(str(self.videoInfo.tmpPath))

        # 创建 过滤后的视频文件
        size = (int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps = self.video.get(cv2.CAP_PROP_FPS) * 1.046
        self.out = cv2.VideoWriter(str(self.videoInfo.filterFile), cv2.VideoWriter_fourcc(*'H264'), fps, size)

        self.canFastFind = False
        self.lastPoint = [0, 0]
        self.size = 20

    def coverImage(self):
        # construct the argument parse and parse the arguments

        # start the file video stream thread and allow the buffer to
        # start to fill
        print("[INFO] starting video file thread..." + str(self.videoInfo.tmpPath))
        fvs = FileVideoStream(str(self.videoInfo.tmpPath)).start()
        time.sleep(1.0)

        # start the FPS timer
        fps = FPS().start()

        # loop over frames from the video file stream
        self.find_count = 0
        index = 0
        while fvs.more():
            index = index + 1
            print(index)

            frame = fvs.read()

            p1, p2 = self.find_logo(frame)

            self.draw_logo(frame, p1, p2)

            self.out.write(frame)

            fps.update()

        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # do a bit of cleanup
        fvs.stop()
        self.video.release()
        self.out.release()

    def find_logo(self, frame):
        if self.canFastFind:
            frame = self.copyImage(frame)

        mask = img2HSV(frame)
        result = cv2.matchTemplate(mask, self.target, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        p1 = max_loc
        if self.canFastFind:
            p1 = [(self.lastPoint[0] - self.size) + p1[0], (self.lastPoint[1] - self.size) + p1[1]]

        if p1[0] != 0 and p1[1] != 0 and self.get_distant(self.lastPoint, p1) < 10 and not self.canFastFind:
            self.find_count = self.find_count + 1
            self.lastPoint = p1
            if self.find_count > 6:
                self.canFastFind = True

        p2 = (p1[0] + self.tw, p1[1] + self.th)
        return p1, p2

    def copyImage(self, frame):
        w, h = self.lastPoint
        return frame[(w - self.size):(h - self.size), (w + self.tw + self.size):(h + self.th + self.size)]

    def get_distant(self, p1, p2):
        p3 = np.array(p2) - np.array(p1)
        return math.hypot(p3[0], p3[1])

    # 画 logo
    def draw_logo(self, frame, p1, p2):
        cv2.rectangle(frame, p1, p2, (255, 255, 255), thickness=cv2.FILLED)
        cv2.putText(frame, "Deemons", (p1[0], p1[1] + int(self.th * 0.75)), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (144, 144, 144), 2)

    def handle(self):
        mp3 = video2mp3(str(self.videoInfo.tmpPath))
        outfile = video_add_mp3(str(self.videoInfo.filterFile), mp3)

        os.rename(str(self.videoInfo.tmpPath), self.videoInfo.src)

        # os.remove(str(self.videoInfo.filterFile))
        # os.remove(mp3)

        # path, newName = FileUtils.getOtherFilePath(self.filePath, "视频去水印")
        # print(outfile)
        # shutil.move(outfile, path)
        # os.rename(os.path.join(path, os.path.split(outfile)[1]), os.path.join(path, os.path.split(self.filePath)[1]))


class VideoInfo:

    def __init__(self, src):
        self.src = src
        self.srcPath = pathlib.Path(src)
        self.srcName = self.srcPath.name
        self.srcParentPath = self.srcPath.parent
        self.tmpName = str(int(time.time()))
        self.tmpPath = self.srcParentPath / self.tmpName
        self.filterFile = self.srcParentPath / (self.tmpName + ".avi")


def img2HSV(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 90, 60])  # 所要检测的像素范围
    upper = np.array([11, 260, 260])  # 此处检测绿色区域
    mask = cv2.inRange(hsv, lowerb=lower, upperb=upper)
    return mask


def video2mp3(file_name):
    outfile_name = file_name.split('.')[0] + '.mp3'
    mp4_version = AudioSegment.from_file(file_name) + 16
    mp4_version.export(outfile_name, format="mp3")
    return outfile_name


def video_add_mp3(file_name, mp3_file):
    outfile_name = file_name.split('.')[0] + '-f.mp4'
    subprocess.call(
        'ffmpeg -y -i ' + file_name + ' -i ' + mp3_file + ' -c:v copy -c:a aac -strict experimental ' + outfile_name,
        shell=True)
    return outfile_name


def video_format(file_name):
    split = file_name.split('.')
    outfile_name = split[0] + '-t.' + split[1]
    subprocess.call(
        'ffmpeg -y -i ' + file_name + ' -r 30 -b 600k ' + outfile_name,
        shell=True)
    # os.remove(file_name)
    # os.rename(outfile_name, file_name)


def doSigleTask(file, imageTarget):
    filter(file, imageTarget).start()


def doAllTask(path):
    fileList = FileUtils.getFile(path, '.mp4')

    pool = Pool(12)
    image = img2HSV(cv2.imread("test2.png", cv2.IMREAD_UNCHANGED))
    for file in fileList:
        pool.apply_async(doSigleTask(file, image))

    pool.close()
    pool.join()


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


def do(path):
    record = filter(path, "test2.png")
    record.start()


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

# 19.882164800942682
# 31496.0

# 18.99999095123621
# 31496.0
if __name__ == '__main__':
    record = filter('/Users/deemons/PycharmProjects/ScrennRecording/main/filter/1.画册的基本概念.mp4', img2HSV(cv2.imread("test2.png", cv2.IMREAD_UNCHANGED)))
    record.start()

    # video = cv2.VideoCapture('/Users/deemons/PycharmProjects/ScrennRecording/main/filter/6-图层打组及复制对象.mp4')
    # print(video.get(5))
    # print(video.get(7))

    # doAllTask('/Users/deemons/PycharmProjects/ScrennRecording/main/filter')
    # print("main===>> " + threading.current_thread().name)

    # hsv = cv2.cvtColor(cv2.imread("test2.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2HSV)
    # lower = np.array([0, 130, 60])  # 所要检测的像素范围
    # upper = np.array([11, 260, 260])  # 此处检测颜色区域
    # mask = cv2.inRange(hsv, lowerb=lower, upperb=upper)
    # cv2.imshow("mask", mask)

    # getHSV()

    # cv2.imshow("", img2HSV(cv2.imread("test2.png", cv2.IMREAD_UNCHANGED)))
    #
    # cv2.waitKey(0)
