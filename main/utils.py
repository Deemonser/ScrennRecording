#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Video(object):
    def __init__(self, path):
        self.path = path

    def play(self):
        from os import startfile
        startfile(self.path)


class Movie_MP4(Video):
    type = 'MP4'


from pynput.mouse import Button, Controller
import time

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


if __name__ == '__main__':
    movie = Movie_MP4(r'C:\Users\Deemons\Desktop\20181107_223803.mp4')
    files = getFile(r'C:\Users\Deemons\Desktop', '.mp4')
    print(files)
    # movie.play()
