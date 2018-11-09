#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from moviepy.editor import VideoFileClip
import os
import pyautogui
from main import Screen


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
        x, y = Screen.getPosition('./image/fullScreenButton.png')
        pyautogui.click(x, y)

    def closeWindow(self):
        pyautogui.press("esc")
        x, y = Screen.getPosition('./image/closePlayer.png')
        pyautogui.click(x, y)


class Movie_MP4(Video):
    type = 'MP4'
