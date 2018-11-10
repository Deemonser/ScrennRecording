import tkinter

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


class mainActivity:

    def show(self):
        window = tkinter.Tk()
        window.title("录屏脚本")
        screenwidth = window.winfo_screenwidth()
        screenheight = window.winfo_screenheight() - 100
        window.geometry('500x300+500+300')

        titleFm = Frame(window)
        tkinter.Label(titleFm, text='目录').pack(side=TOP, anchor='w', pady=10)
        tkinter.Label(titleFm, text='文件后缀').pack(side=TOP, anchor='w', pady=2)
        tkinter.Label(titleFm, text='录屏软件').pack(side=TOP, anchor='w', pady=2)
        tkinter.Label(titleFm, text='识别时长').pack(side=TOP, anchor='w', pady=2)
        titleFm.pack(side=LEFT, anchor='n')

        contentFm = Frame(window)
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
        self.duringImagePath = StringVar()
        self.duringImagePath.set(r'/Users/deemons/PycharmProjects/ScrennRecording/main/image/xunhuan.png')
        image_open = Image.open(self.duringImagePath.get())

        self.duringImage = ImageTk.PhotoImage(image_open)
        self.duringButton = tkinter.Button(itemFm, text=" 时长定位点 ", image=self.duringImage,
                                           command=self.chooseDuringImagePath, width=30)
        self.duringButton.pack(side=LEFT)
        self.duringX = StringVar()
        self.duringX.set("0")
        self.duringY = StringVar()
        self.duringY.set("0")
        tkinter.Label(itemFm, text="X 轴偏移", anchor='e').pack(side=LEFT, padx=10)
        tkinter.Entry(itemFm, textvariable=self.duringX, width=5).pack(side=LEFT)
        tkinter.Label(itemFm, text="Y 轴偏移").pack(side=LEFT, padx=5)
        tkinter.Entry(itemFm, textvariable=self.duringY, width=5).pack(side=LEFT)
        itemFm.pack(side=LEFT, anchor='w', pady=1)

        # 进入消息循环
        window.mainloop()

    def chooseFile(self):
        f = filedialog.askdirectory()
        if not f == "":
            self.path.set(f)

    def chooseExt(self):
        f = filedialog.askopenfilename(filetypes=[('EXE', 'exe')])
        if not f == "":
            self.record.set(f)

    def chooseDuringImagePath(self):
        f = filedialog.askopenfilename(filetypes=[('PNG', 'png'), ('JPEG', 'jpeg')])
        if not f == "":
            self.duringImagePath.set(f)
            # self.duringImage1 = ImageTk.PhotoImage(Image.open(self.duringImagePath.get()))
            # self.duringButton.configure(image=self.duringImager1)


if __name__ == '__main__':
    mainActivity().show()
