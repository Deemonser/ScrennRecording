import time, os
# https://www.jianshu.com/p/552f96aa85dc

from main.utils import getFile, Movie_MP4
from pykeyboard import PyKeyboard


class record:

    def __init__(self, path, during):
        self.path = path
        self.during = during
        self.k = PyKeyboard()

    def startRecording(self):
        self.k.press_key(self.k.alt_key)
        self.k.tab_key(self.k.function_keys[1])
        self.k.redo_key(self.k.alt_key)

    def stopRecording(self):
        self.k.press_key(self.k.alt_key)
        self.k.tab_key(self.k.function_keys[2])
        self.k.redo_key(self.k.alt_key)
        time.sleep(500)
        self.k.type_string(self.path)
        self.k.tab_key()


if __name__ == '__main__':
    files = getFile(r'../../', '.itcast')
    rate = 5000 / 5
    print(files)

    for file in files:
        movie = Movie_MP4(file)
        print(str(movie.getSize()))
        during = movie.getDuringByRate(rate)
        print(str(during))
        record = record(os.path.split(file), during)
        record.startRecording()
        movie.play()
        time.sleep(during)
        record.stopRecording()

    print(time.time())
    print(time.time())
