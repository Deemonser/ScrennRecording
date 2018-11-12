import threading
import tkinter

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import json
from main.Control import Control
from main.data import settingBean


class mainActivity:

    def __init__(self):
        settingBean.getSettingData()

    def show(self):
        self.isStart = False
        self.window = tkinter.Tk()
        self.window.title("录屏脚本")
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight() - 100
        self.window.geometry('500x300+500+300')

        self.startButton = tkinter.Button(self.window, text='开始', command=self.start, width=10, height=2)
        self.startButton.pack(side=BOTTOM)

        titleFm = Frame(self.window)
        tkinter.Label(titleFm, text='视频目录').pack(side=TOP, anchor='w', pady=10)
        tkinter.Label(titleFm, text='视频后缀').pack(side=TOP, anchor='w', pady=2)
        tkinter.Label(titleFm, text='录屏软件').pack(side=TOP, anchor='w', pady=2)
        tkinter.Label(titleFm, text='播放时长\n显示区域').pack(side=TOP, anchor='w', pady=6)
        tkinter.Label(titleFm, text='播放器\n功能按钮').pack(side=TOP, anchor='w', pady=16)
        titleFm.pack(side=LEFT, anchor='n')

        contentFm = Frame(self.window)
        contentFm.pack(side=LEFT, anchor='n', padx=3)
        # 目录
        itemFm = Frame(contentFm)
        self.path = StringVar()
        self.path.set("c:\\User\\Deemons\\Desktop")
        tkinter.Entry(itemFm, textvariable=self.path, width=40).pack(side=LEFT)
        tkinter.Button(itemFm, text=" ... ", command=self.chooseFile).pack(side=LEFT)
        itemFm.pack(side=TOP, anchor='w', pady=6)
        # 后缀
        itemFm = Frame(contentFm)
        self.endName = StringVar()
        self.endName.set(".itcase")
        tkinter.Entry(itemFm, textvariable=self.endName, width=10).pack(side=LEFT)
        itemFm.pack(side=TOP, anchor='w')

        # 录屏软件位置
        itemFm = Frame(contentFm)
        self.record = StringVar()
        self.record.set("C:\\User\\Deemons\\Desktop\\Evcapture.exe")
        tkinter.Entry(itemFm, textvariable=self.record, width=40).pack(side=LEFT)
        tkinter.Button(itemFm, text=" ... ", command=self.chooseExt).pack(side=LEFT)
        itemFm.pack(side=TOP, anchor='w', pady=1)

        # 识别时长
        itemFm = Frame(contentFm)
        itemFm.pack(side=TOP, anchor='w', pady=1)
        self.duringImagePath = r'/Users/deemons/PycharmProjects/ScrennRecording/main/image/player_2/player_during.png'
        image_open = Image.open(self.duringImagePath)
        self.duringImage = ImageTk.PhotoImage(image_open)
        self.duringButton = tkinter.Button(itemFm, text=" 时长定位点 ", image=self.duringImage,
                                           command=self.chooseDuringImagePath
                                           , width=50, height=50)
        self.duringButton.pack(side=LEFT)

        childFm = Frame(itemFm)
        self.duringWidth = IntVar()
        self.duringWidth.set(150)
        tkinter.Label(childFm, text="区域宽度", anchor='e').pack(side=LEFT, padx=10)
        tkinter.Entry(childFm, textvariable=self.duringWidth, width=5).pack(side=LEFT)

        self.duringX = IntVar()
        self.duringX.set(30)
        tkinter.Label(childFm, text="X 偏移", anchor='e').pack(side=LEFT, padx=10)
        tkinter.Entry(childFm, textvariable=self.duringX, width=5).pack(side=LEFT)
        childFm.pack(side=TOP, anchor='w')

        childFm = Frame(itemFm)
        self.duringHeight = IntVar()
        self.duringHeight.set(40)
        tkinter.Label(childFm, text="区域高度", anchor='e').pack(side=LEFT, padx=10)
        tkinter.Entry(childFm, textvariable=self.duringHeight, width=5).pack(side=LEFT)

        self.duringY = IntVar()
        self.duringY.set(0)
        tkinter.Label(childFm, text="Y 偏移", anchor='e').pack(side=LEFT, padx=10)
        tkinter.Entry(childFm, textvariable=self.duringY, width=5).pack(side=LEFT)
        childFm.pack(side=TOP, anchor='w')

        itemFm = Frame(contentFm)
        itemFm.pack(fill='x', anchor='s', pady=1)

        # 播放按钮
        childFm = Frame(itemFm)
        self.playerPlayPath = r'/Users/deemons/PycharmProjects/ScrennRecording/main/image/player_2/player_play.png'
        self.playImage = ImageTk.PhotoImage(Image.open(self.playerPlayPath))
        self.playButton = tkinter.Button(childFm, image=self.playImage, command=self.choosePlayerImagePath
                                         , width=40, height=40)
        self.playButton.pack(side=TOP)
        tkinter.Label(childFm, text="播放按钮", anchor='e').pack(side=TOP, padx=10)
        childFm.pack(side=LEFT, anchor='w')

        # 全屏按钮
        childFm = Frame(itemFm)
        self.playerFullPath = r'/Users/deemons/PycharmProjects/ScrennRecording/main/image/player_2/player_full.png'
        self.fullImage = ImageTk.PhotoImage(Image.open(self.playerFullPath))
        self.fullButton = tkinter.Button(childFm, image=self.fullImage, command=self.choosePlayerImagePath
                                         , width=40, height=40)
        self.fullButton.pack(side=TOP)

        tkinter.Label(childFm, text="全屏按钮", anchor='e').pack(side=TOP, padx=10)
        childFm.pack(side=LEFT, anchor='w')

        # 关闭按钮
        childFm = Frame(itemFm)
        self.playerClosePath = r'/Users/deemons/PycharmProjects/ScrennRecording/main/image/player_2/player_close.png'
        self.closeImage = ImageTk.PhotoImage(Image.open(self.playerClosePath))
        self.closeButton = tkinter.Button(childFm, image=self.closeImage, command=self.chooseCloseImagePath
                                          , width=40, height=40)
        self.closeButton.pack(side=TOP)

        tkinter.Label(childFm, text="关闭按钮", anchor='e').pack(side=TOP, padx=10)
        childFm.pack(side=LEFT, anchor='w')

        # 进入消息循环
        self.window.mainloop()

    def chooseFile(self):
        f = filedialog.askdirectory()
        if not f == "":
            self.path.set(f)

    def chooseExt(self):
        f = filedialog.askopenfilename(filetypes=[('EXE', 'exe')])
        if not f == "":
            self.record.set(f)

    def chooseDuringImagePath(self):
        f = filedialog.askopenfilename(filetypes=[('PNG', 'png'), ('JPEG', 'jpeg'), ('JPG', 'jpg')])
        if not f == "":
            self.duringImagePath = f
            self.duringImage = ImageTk.PhotoImage(Image.open(self.duringImagePath))
            self.duringButton.configure(image=self.duringImage)
            self.window.update_idletasks()

    def choosePlayerImagePath(self):
        f = filedialog.askopenfilename(filetypes=[('PNG', 'png'), ('JPEG', 'jpeg'), ('JPG', 'jpg')])
        if not f == "":
            self.playerPlayPath = f
            self.playImage = ImageTk.PhotoImage(Image.open(self.playerPlayPath))
            self.playButton.configure(image=self.playImage)
            self.window.update_idletasks()

    def chooseFullImagePath(self):
        f = filedialog.askopenfilename(filetypes=[('PNG', 'png'), ('JPEG', 'jpeg'), ('JPG', 'jpg')])
        if not f == "":
            self.playerFullPath = f
            self.fullImage = ImageTk.PhotoImage(Image.open(self.playerFullPath))
            self.fullButton.configure(image=self.fullImage)
            self.window.update_idletasks()

    def chooseCloseImagePath(self):
        f = filedialog.askopenfilename(filetypes=[('PNG', 'png'), ('JPEG', 'jpeg'), ('JPG', 'jpg')])
        if not f == "":
            self.playerclosePath = f
            self.closeImage = ImageTk.PhotoImage(Image.open(self.playerclosePath))
            self.closeButton.configure(image=self.closeImage)
            self.window.update_idletasks()

    def start(self):
        if not self.isStart:
            self.isStart = True
            control = Control(r'F:\UI设计-基础班\【第1天】Photoshop基础\1-视频', '.itcast', 1.0)
            threading.Thread(target=control.doAllTask()).start()
        else:
            exit()


if __name__ == '__main__':
    mainActivity().show()
