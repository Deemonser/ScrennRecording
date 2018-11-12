#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

import os, time
import pyautogui
from PIL import Image

from main import Screen, ImageUtils, timeUtils
from aip import AipOcr
from main.ImageUtils import *


class Video(object):
    def __init__(self, path):
        self.path = path
        self.width, self.height = pyautogui.size()
        print("video play file: %s" % (self.path))

    def getSize(self):
        return os.path.getsize(self.path)

    def getDuringByRate(self, rate):
        return self.getSize() / rate

    def play(self):
        os.startfile(self.path)
        pyautogui.click(Screen.getPosition('./image/player_1/player_play.png'))

    def fullWindow(self):
        # pyautogui.click(Screen.getPosition('./image/player_full.png'))
        pyautogui.click(Screen.getPosition('./image/player_1/player_full.png'))
        pyautogui.press("left", 3)
        pyautogui.moveTo(self.width / 2, self.height - 20)
        # pyautogui.click(Screen.getPosition('./image/player_1/player_stop.png'))
        # time.sleep(0.5)

        pyautogui.press("space")
        # pyautogui.press("space")
        print("full window")

    def prepare(self):
        pyautogui.moveRel(None, -self.height / 2)
        time.sleep(2)
        print("prepare")

    def getDuring(self):
        timeInfo = ImageUtils.ocr(
            image_to_bytes(screenshotByImage('./image/player_1/player_during.png', 15, -15, 150, 40)))
        during = timeUtils.handleOcrTime(timeInfo['words_result'][0]['words'].split('/'))
        print(during)
        return during

    def start(self):
        pyautogui.press("space")
        print("start")

    def closeWindow(self):
        pyautogui.hotkey("alt","f4")
        # pyautogui.press("esc")
        # pyautogui.click(Screen.getPosition('./image/player_1/player_close.png'))


class Movie_MP4(Video):
    type = 'MP4'
