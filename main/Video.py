#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

import os, time
import pyautogui
from main import Screen, ImageUtils, timeUtils
from aip import AipOcr
from main.ImageUtils import *

import base64
from io import BytesIO

APP_ID = '14751225'
API_KEY = 'fKdnAilSeCIcWrs7GDtGz4xG'
SECRET_KEY = 'WdiYaotcRRAUb9yfDsEGX84OZ6wbwuNq'


class Video(object):
    def __init__(self, path):
        self.path = path
        self.api = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    def getSize(self):
        return os.path.getsize(self.path)

    def getDuringByRate(self, rate):
        return self.getSize() / rate

    def play(self):
        os.startfile(self.path)

    def fullWindow(self):
        # pyautogui.click(Screen.getPosition('./image/fullScreenButton.png'))
        pyautogui.click(Screen.getPosition('./image/fullScreen.png'))
        time.sleep(0.5)
        pyautogui.click(Screen.getPosition('./image/player_stop.png'))
        pyautogui.click(Screen.getPosition('./image/player_play.png'))
        pyautogui.press("space")

    def prepare(self):
        pyautogui.moveRel(None, 200)
        time.sleep(2)

    def getDuring(self):
        timeInfo = ImageUtils.ocr(image_to_bytes(screenshotByImage('./image/xunhuan.png', 15, -15, 150, 40)))
        during = timeUtils.handleOcrTime(timeInfo['words_result'][0]['words'].split('/'))
        print(during)
        return during

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def image_to_base64(self, img):
        output_buffer = BytesIO()
        img.save(output_buffer, format='PNG')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        return base64_str

    def start(self):
        pyautogui.press("space")

    def closeWindow(self):
        pyautogui.press("esc")
        pyautogui.click(Screen.getPosition('./image/closePlayer.png'))


class Movie_MP4(Video):
    type = 'MP4'
