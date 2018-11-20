import sys

import os

import json

sys.path.append(os.path.abspath(".") + "/InFile/")


class settingBean:

    # 读取数据
    def getSettingData(self):
        print(os.getcwd())
        with open(r'../data/setting.json', 'r') as f:
            data = json.load(f)
            f.close()
        return data

    # 写入 JSON 数据
    def setSettingData(self, data):
        with open('setting.json', 'w') as f:
            json.dump(data, f)
            f.close()
