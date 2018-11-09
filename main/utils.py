#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from moviepy.editor import VideoFileClip


class Video(object):
    def __init__(self, path):
        self.path = path

    def getDuring(self):
        return VideoFileClip(self.path).duration

    def getSize(self):
        return os.path.getsize(self.path)

    def getDuringByRate(self, rate):
        return self.getSize() / rate

    def play(self):
        from os import startfile
        startfile(self.path)


class Movie_MP4(Video):
    type = 'MP4'


from pynput.mouse import Button, Controller as Mouse
from pynput.keyboard import Key, Controller as Keyboard
import time
import pyautogui

# mouse = Controller()
# print(mouse.position)
# time.sleep(3)
# print('The current pointer position is {0}'.format(mouse.position))
#
# # set pointer positon
# mouse.position = (277, 645)
# print('now we have moved it to {0}'.format(mouse.position))
#
# # 鼠标移动（x,y）个距离
# mouse.move(5, -5)
# print(mouse.position)
#
# mouse.press(Button.left)
# mouse.release(Button.left)
#
# # Double click
# mouse.click(Button.left, 1)
#
# # scroll two  steps down
# mouse.scroll(0, 500)

# -*- encoding:utf-8 -*-
import os


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


class record:

    def __init__(self, path, during):
        self.path = str(path).replace(str(os.path.splitext(path)[1]), ".mp4")
        self.during = during
        self.k = Keyboard()

    def startRecording(self):
        self.k.press(Key.ctrl_l)
        self.k.press(Key.f1)
        self.k.release(Key.f1)
        self.k.release(Key.ctrl_l)

    def stopRecording(self):
        self.k.press(Key.ctrl_l)
        self.k.press(Key.f2)
        self.k.release(Key.f2)
        self.k.release(Key.ctrl_l)
        print(self.path)
        time.sleep(1)
        self.k.type(self.path)
        self.k.press(Key.enter)
        self.k.release(Key.enter)


if __name__ == '__main__':
    files = getFile(r'../../', '.itcast')
    rate = 5000000 / 5
    print(files)





    # for file in files:
    #     movie = Movie_MP4(file)
    #     print(str(movie.getSize()))
    #     during = movie.getDuringByRate(rate)
    #     print(str(during))
    #     record = record(os.path.split(file)[1], during)
    #     record.startRecording()
    #     movie.play()
    #     time.sleep(during)
    #     record.stopRecording()

    print(time.time())
