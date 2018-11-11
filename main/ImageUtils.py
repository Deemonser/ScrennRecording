import os

import pyautogui
from main import Screen
from aip import AipOcr
import base64
from io import BytesIO

APP_ID = '14751225'
API_KEY = 'fKdnAilSeCIcWrs7GDtGz4xG'
SECRET_KEY = 'WdiYaotcRRAUb9yfDsEGX84OZ6wbwuNq'

api = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def screenshotByImage(imagePath, offx, offy, width, height):
    x, y = Screen.getPosition(imagePath)
    print("during position=%d , %d" % (x, y))
    return pyautogui.screenshot(region=(x + offx, y + offy, width, height))


def ocr(image):
    timeInfo = api.basicGeneral(image)
    print(timeInfo)
    return timeInfo


def get_file_bytes(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def image_to_bytes(img):
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    return byte_data


def getImagePath(path=''):
    return os.path.join(os.getcwd(), path)


if __name__ == '__main__':
    # ocr(image_to_bytes(screenshotByImage('./image/xunhuan.png', 15, -15, 150, 40)))
    print(getImagePath("image"))
