#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from moviepy.editor import VideoFileClip
import os


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
        os.startfile(self.path)

    def fullWindow(self):
        print("全屏")


    def closeWindow(self):
        print("关闭")


class Movie_MP4(Video):
    type = 'MP4'
