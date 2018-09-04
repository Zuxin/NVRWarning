import sys
import requests
import time
import pygame
import json
import logging
import getNVR
from itertools import chain
from PyQt5.QtWidgets import QApplication, QMainWindow
from firstMainWin import Ui_mainWindow
from PyQt5.QtCore import QTimer, QDateTime, pyqtSignal, QThread

url = r"http://127.0.0.1:8888/upload_to_tegu"  # 连接tegu
files = {'file': (r'cache.png', open('cache.png', 'rb'), 'image/png', {})}  # 上传用缓存文件
humanWarning = "person"  # 出现人的警告信息
hydrantWarning = "hydrant"  # 消防设备警告信息
sleepTime = 10  # 每次取视频的循环间隔时间
file = "warning.mp3"  # 警报音


# 播放警告音乐
def play_warning_music():
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    time.sleep(10)
    pygame.mixer.music.stop()


class MyMainWindow(QMainWindow, Ui_mainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置定时器将定时器的信号与槽链接
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        # 设置时间间隔并启动
        self.timer.start(1000)
        self.init_messages()

    def init_messages(self):
        # 创建线程并连接信号槽
        self.getmessage = BackendThread()
        self.getmessage.warning.connect(self.show_message)
        self.getmessage.start()

    # 显示时间
    def show_time(self):
        time = QDateTime.currentDateTime()
        time_display = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.label_3.setText(time_display)

    # 警告信息
    def show_message(self, data):
        # print(data)
        if data.startswith("1"):
            self.label.setText(data)
            self.setStyleSheet('''
            #label { color: red }
                                    ''')
            play_warning_music()
        elif data.startswith("2"):
            self.label.setText(data)
            self.setStyleSheet('''
            #label { color: red }
                                     ''')
            play_warning_music()
        elif data.startswith("3") or data.startswith("4"):
            self.label.setText(data)
            self.setStyleSheet('''
            #label { color: orange }
                                    ''')
        elif data == "正常":
            self.label.setText(data)
            self.setStyleSheet('''
                #label { color: green; 
                }
                ''')


# 子线程处理后台逻辑防止堵塞
class BackendThread(QThread):
    # 通过类成员定义信号
    warning = pyqtSignal(str)

    # 将返回的信号进行检验
    def run(self):
        # 定义视频信号源
        getNVR.define_captures()
        while True:
            # 监测摄像头连接是否为空如果为空则大概率为网络问题
            if getNVR.captures:
                # 测试是否能连接tegu
                try:
                    r = requests.get(url)
                    r.encoding = "utf-8"
                    global state
                    state = r.status_code
                except (ValueError,
                        ConnectionError, requests.HTTPError, requests.Timeout, requests.TooManyRedirects) as e:
                    state = 404
                    logging.exception(e)
                    self.warning.emit("4网络连接错误")
                else:
                    state = 404
                    self.warning.emit("4网络连接错误")
                if state == 200:
                    # 将每个摄像头信息传入tegu进行监测
                    for cam_id, cam_capture in getNVR.captures:
                        global cam_id
                        # 判断摄像头是否正常工作
                        if cam_capture is not None:
                            # 生成缓存文件以监测
                            getNVR.make_cache(cam_capture)
                            # 用post方法将缓存图片传入tegu
                            r = requests.post(url, files=files)
                            # 获得json文件然后读取
                            info = json.loads(r.content)
                            # 判断返回情况只有晚上才开始判断,将返回的嵌套列表flatten然后查看是否含有元素
                            if humanWarning in list(chain.from_iterable(info)) and (
                                    int(time.strftime("%H")) > 22 or int(time.strftime("%H")) < 7):
                                self.warning.emit("1警告，监测到" + cam_id + "号摄像头有人出没")
                            elif hydrantWarning in list(chain.from_iterable(info)):
                                self.warning.emit("2警告，监测到" + cam_id + "号摄像头有消防设备移动")
                            else:
                                self.warning.emit("正常")
                else:
                    self.warning.emit("3" + cam_id + "号摄像头连接失败" + str(state))
                # SleepTime秒后进行监测
                time.sleep(sleepTime)
            else:
                self.warning.emit("4网络连接错误")


if __name__ == "__main__":
    pygame.mixer.init()
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    qssStyle = '''
    #label { color: green; 
    }
    #label_3 { color: blue
    }
        '''
    myWin.setStyleSheet(qssStyle)
    myWin.show()
    sys.exit(app.exec_())
