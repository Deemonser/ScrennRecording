import json

setting = {
    'path': r'c:\User\Deemons\Desktop',
    'endName': r'.itcase',
    'recordPath': r'C:\User\Deemons\Desktop\Evcapture.exe',
    'duringImagePath': r'C:\User\Deemons\Desktop\Evcapture.exe',

}


# 读取数据
def getSettingData():
    with open('setting.json', 'r') as f:
        data = json.load(f)
    if data == None:
        data = setting
        setSettingData(data)
    return data


# 写入 JSON 数据
def setSettingData(data):
    with open('setting.json', 'w') as f:
        json.dump(data, f)
