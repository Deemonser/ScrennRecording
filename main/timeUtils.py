


def handleOcrTime(timeInfo):
    if timeInfo.__contains__('/'):
        return t2s(timeInfo.split('/')[1])
    else:
        len = timeInfo.__len__()
        return t2s(timeInfo[int(len / 2):len][0])


def t2s(t):
    print(t)
    list = t.strip().split(":")
    h, m, s = 0, 0, 0
    if list.__len__() == 3:
        h, m, s = list
    elif list.__len__() == 2:
        m, s = list

    return int(h) * 3600 + int(m) * 60 + int(s)


if __name__ == '__main__':
    handleOcrTime("00:01/02:36")
