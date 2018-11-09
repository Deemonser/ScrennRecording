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
