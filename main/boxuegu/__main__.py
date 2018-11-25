import boxuegu
import sys

print("starting.........")
try:
    boxuegu.Control().doSingleTask()
except:
    print("Unexpected error:", sys.exc_info())  # sys.exc_info()返回出错信息

input('press enter key to exit')  # 这儿放一个等待输入是为了不让程序退出
print("end")
