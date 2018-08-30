import sys
import requests
import time
import pygame
import json
import logging
import getNVR
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QDialog
from firstMainWin import Ui_mainWindow
from PyQt5.QtCore import QTimer, QDateTime, pyqtSignal, QThread


url = r"http://127.0.0.1:8888/get_"   # 返回地址
humanWarning = ""  # 出现人的警告信息
hydrantWarning = ""  # 消防设备警告信息
# 播放警报音
file = 'warning.mp3'
pygame.mixer.init()
track = pygame.mixer.music.load(file)


class MyMainWindow(QMainWindow, Ui_mainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置定时器将定时器的信号与槽链接
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        # 设置时间间隔并启动
        self.timer.start(1000)
        self.init_caps()
        self.init_ui()

    def init_caps(self):
        self.sendmessage = SendCaptureThread()
        self.sendmessage.start()

    def init_ui(self):
        # 创建线程
        self.backend = BackendThread()
        self.backend.warning.connect(self.show_message)
        self.backend.start()

    # 显示时间
    def show_time(self):
        time = QDateTime.currentDateTime()
        time_display = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.label_3.setText(time_display)

    # 警告信息
    def show_message(self, data):
        # print(data)
        if data == "human":
            self.label.setText("监测到"+info[0][0]+"的摄像头出现人")
            self.setStyleSheet('''
            #label { color: red }
                                    ''')
            pygame.mixer.music.play()
            time.sleep(10)
            pygame.mixer.music.stop()
        # if data == "hydrant":
        #   self.label.setText("监测到"+info[0][0]+"的摄像头出现设备移动")
        #   self.setStyleSheet('''
        #   #label { color: red }
        #                           ''')
        #   pygame.mixer.music.play()
        #   time.sleep(10)
        #   pygame.mixer.music.stop()
        elif data == "error":
            self.label.setText("网络出现错误")
            self.setStyleSheet('''
            #label { color: orange }
                                    ''')
        elif data == "normal":
            self.label.setText("正常")
            self.setStyleSheet('''
                #label { color: green; 
                }
                ''')



class BackendThread(QThread):
    # 通过类成员定义信号
    warning = pyqtSignal(str)

    # 将返回的信号进行检验
    def run(self):
        while True:
            try:
                r = requests.get(url)
                r.encoding = "utf-8"
                state = r.status_code
                global info
                info = json.load(r.content)
            except (ValueError, ConnectionError, requests.HTTPError, requests.Timeout, requests.TooManyRedirects) as e:
                state = 404
                logging.exception(e)
            if state == 200:
                print("连接成功"+str(state))
                if info[0][1] == "human":
                    self.warning.emit("human")
                elif info[0][1] == "hydrant":
                    self.warning.emit("hydrant")
                else:
                    self.warning.emit("normal")
            else:
                print("连接失败"+str(state))
                self.warning.emit("error")
            time.sleep(1)


class SendCaptureThread(QThread):
    # 获取视频信息
    def run(self):
        getNVR.define_captures()
        if getNVR.captures:
            isStarted = True
        else:
            isStarted = False
        getNVR.input_video_capture(isStarted)


if __name__ == "__main__":
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
