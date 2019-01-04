import os, shutil

from pydub import AudioSegment
import subprocess
from imutils.video import FileVideoStream, FPS
import numpy as np
import math
import time
import cv2
import pathlib


class filter:

    def __init__(self, filePath, imagetarget):
        self.filePath = filePath
        # 读取 目标图片
        self.target = img2HSV(cv2.imread(imagetarget, cv2.IMREAD_UNCHANGED))
        # 目标图片的宽高
        self.th, self.tw = self.target.shape[:2]
        self.videoInfo = VideoInfo(self.filePath)

    def start(self):

        self.prepare()

        try:
            self.coverImage()
            outFile = self.handle()
        except Exception as e:
            print(e)

        self.end()

    def end(self):
        os.remove(str(self.videoInfo.tmpPath))

    def prepare(self):
        print('process id:', os.getpid())
        shutil.copy(self.videoInfo.srcPath, self.videoInfo.tmpPath)

        # 创建视频
        self.video = cv2.VideoCapture(str(self.videoInfo.tmpPath))

        # 创建 过滤后的视频文件
        self.src_w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.src_h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        size = (self.src_w, self.src_h)
        self.videoInfo.fps = self.video.get(cv2.CAP_PROP_FPS)
        fps = self.videoInfo.fps * 1.03
        self.out = cv2.VideoWriter(str(self.videoInfo.filterFile), cv2.VideoWriter_fourcc(*'H264'), fps, size)

        self.canFastFind = False
        self.lastPoint = [0, 0]
        self.size = 120

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
        tmpFrame = frame
        if self.canFastFind:
            tmpFrame = self.copyImage(tmpFrame)

        mask = img2HSV(tmpFrame)
        result = cv2.matchTemplate(mask, self.target, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        p1 = max_loc

        if self.canFastFind:
            x = (self.lastPoint[0] - self.size)
            y = (self.lastPoint[1] - self.size)
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            p1 = (x + p1[0], y + p1[1])

        if p1[0] != 0 and p1[1] != 0 and self.get_distant(self.lastPoint, p1) < 20 and not self.canFastFind:
            self.find_count = self.find_count + 1
            if self.find_count > 4:
                self.canFastFind = True
        else:
            self.find_count = 0

        self.lastPoint = p1
        p2 = (p1[0] + self.tw, p1[1] + self.th)
        return p1, p2

    def copyImage(self, frame):
        w, h = self.lastPoint
        w1 = w - self.size
        h1 = h - self.size

        w2 = w + self.tw + self.size
        h2 = h + self.th + self.size

        if w1 < 0:
            w1 = 0
        if h1 < 0:
            h1 = 0
        if w2 > self.src_w:
            w2 = self.src_w
        if h2 > self.src_h:
            h2 = self.src_h

        return frame[(h1):(h2), (w1):(w2)]

    def get_distant(self, p1, p2):
        p3 = np.array(p2) - np.array(p1)
        return math.hypot(p3[0], p3[1])

    # 画 logo
    def draw_logo(self, frame, p1, p2):
        cv2.rectangle(frame, p1, p2, (255, 255, 255), thickness=cv2.FILLED)
        cv2.putText(frame, "Deemons", (p1[0], p1[1] + int(self.th * 0.75)), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (144, 144, 144), 2)

    def handle(self):
        video_format(str(self.videoInfo.filterFile), str(self.videoInfo.fps), str(self.videoInfo.formatMP4))
        mp3 = video2mp3(str(self.videoInfo.tmpPath))
        outFile = video_add_mp3(str(self.videoInfo.formatMP4), mp3)

        # 删除临时视频
        os.remove(str(self.videoInfo.filterFile))
        os.remove(str(self.videoInfo.formatMP4))
        # 删除临时音频
        os.remove(mp3)

        shutil.move(outFile, self.videoInfo.outFile)

        return outFile


class VideoInfo:

    def __init__(self, src):
        self.fps = None
        self.src = src
        self.srcPath = pathlib.Path(src)
        self.srcName = self.srcPath.name
        self.srcParentPath = self.srcPath.parent
        self.tmpName = str(int(time.time()))
        self.tmpPath = self.srcParentPath / self.tmpName
        self.filterFile = self.srcParentPath / (self.tmpName + ".avi")
        self.formatMP4 = self.srcParentPath / (self.tmpName + "-f.mp4")
        self.tmpMP3 = self.srcParentPath / (self.tmpName + ".mp3")
        self.tmpMP4 = self.srcParentPath / (self.tmpName + "-t.mp4")
        path, newName = getOtherFilePath(self.src, self.srcParentPath.name + '_filter')
        self.outFile = os.path.join(path, newName)


def getFile(path, text):
    fileList = []
    searchFile(fileList, path, text)
    return fileList


def searchFile(fileList, path, text):
    try:
        files = os.listdir(path)
        for f in files:
            fl = os.path.join(path, f)
            if os.path.isdir(fl):
                # print fl
                searchFile(fileList, fl, text)
            elif os.path.isfile(fl) and os.path.splitext(fl)[1] == text:
                fileList.append(fl)
    except Exception:
        ""


def getOtherFilePath(filePath, otherFileName):
    path = os.path.join(os.path.dirname(os.path.dirname(filePath)), otherFileName)
    if not os.path.exists(path):
        os.makedirs(path)
    srcName = os.path.split(filePath)[1]
    return path, srcName


def img2HSV(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 220, 210])  # 所要检测的像素范围
    upper = np.array([3, 260, 260])  # 此处检测绿色区域
    mask = cv2.inRange(hsv, lowerb=lower, upperb=upper)
    return mask


def video2mp3(file_name):
    outfile_name = file_name.split('.')[0] + '.mp3'
    mp4_version = AudioSegment.from_file(file_name) + 16
    mp4_version.export(outfile_name, format="mp3")
    return outfile_name


def video_add_mp3(file_name, mp3_file):
    outfile_name = file_name.split('.')[0] + '-t.mp4'
    subprocess.call(
        'ffmpeg -y -i ' + file_name + ' -i ' + mp3_file + ' -c:v copy -c:a aac -strict experimental ' + outfile_name,
        shell=True)
    return outfile_name


def video_format(file_name, fps, out_file):
    split = file_name.split('.')
    subprocess.call(
        'ffmpeg -y -threads 4 -r ' + fps + ' -i ' + file_name + ' ' + out_file,
        shell=True)


def doSigleTask(fil):
    fil.start()
    fil.end()


def doAllTask(path):
    fileList = getFile(path, '.mp4')
    print(fileList)

    for file in fileList:
        try:
            fil = filter(file, "test3.png")
            fil.start()
        except Exception as e:
            print(e)
    # while True:
    #     out, frame = queue.get()
    #     out.write(frame)


def getpos(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(HSV[y, x])


mat = cv2.imread("test.png", cv2.IMREAD_UNCHANGED)
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

# 19.882164800942682
# 31496.0

# 19.91575965409274
# 8905.0
# 19.91576
# 8869.0
if __name__ == '__main__':
    # record = filter('/Users/deemons/PycharmProjects/ScrennRecording/main/filter/1.画册的基本概念.mp4',
    #                 img2HSV(cv2.imread("test2.png", cv2.IMREAD_UNCHANGED)))
    # record.start()

    # video = cv2.VideoCapture('/Users/deemons/PycharmProjects/ScrennRecording/main/filter/out.mp4')
    # print(video.get(5))
    # print(video.get(7))

    doAllTask('/Volumes/shirly/UI/tmp12')


    # print("main===>> " + threading.current_thread().name)

    # hsv = cv2.cvtColor(cv2.imread("test2.png", cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2HSV)
    # lower = np.array([0, 130, 60])  # 所要检测的像素范围
    # upper = np.array([11, 260, 260])  # 此处检测颜色区域
    # mask = cv2.inRange(hsv, lowerb=lower, upperb=upper)
    # cv2.imshow("mask", mask)

    # getHSV()

    # cv2.imshow("", img2HSV(cv2.imread("test333.png", cv2.IMREAD_UNCHANGED)))
    #
    # cv2.waitKey(0)
