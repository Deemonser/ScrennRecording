#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from moviepy.editor import VideoFileClip
import os, time
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
        # pyautogui.click(Screen.getPosition('./image/fullScreenButton.png'))
        pyautogui.click(Screen.getPosition('./image/fullScreen.png'))
        time.sleep(0.5)
        pyautogui.click(Screen.getPosition('./image/player_stop.png'))
        pyautogui.click(Screen.getPosition('./image/player_play.png'))
        pyautogui.press("space")
        pyautogui.moveRel(None, 200)
        time.sleep(2)

    def start(self):
        pyautogui.press("space")

    def closeWindow(self):
        pyautogui.press("esc")
        pyautogui.click(Screen.getPosition('./image/closePlayer.png'))


class Movie_MP4(Video):
    type = 'MP4'
