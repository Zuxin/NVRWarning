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


class MyMainWindow(QMainWindow, Ui_mainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置定时器将定时器的信号与槽链接
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        # 设置时间间隔并启动
        self.timer.start(1000)
        self.init_UI()

    def init_UI(self):
        # 创建线程
        self.backend = BackendThread()
        # 连接信号
        self.backend.warning.connect(self.show_message)
        # 开始线程
        self.backend.start()

    # 显示时间
    def show_time(self):
        time = QDateTime.currentDateTime()
        time_display = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.label_3.setText(time_display)

    # 警告信息
    def show_message(self, message):
        print(message)
        if message == "正常":
            self.label.setText(message)
            self.setStyleSheet('''
                #label { color: green; 
                }
                ''')
        elif "警告" in message:
            self.label.setText(message)
            self.setStyleSheet('''
            #label { color: red }
                                    ''')
            # 播放警告音乐
            pygame.mixer.music.play()
        else:
            self.label.setText(message)
            self.setStyleSheet('''
            #label { color: orange }
                                    ''')


# 子线程处理后台逻辑防止堵塞
class BackendThread(QThread):
    # 通过类成员定义信号
    warning = pyqtSignal(str)
    '''
    # 测试用代码
    def run(self):
        # 测试是否能连接tegu
        try:
            re = requests.get(url)
            re.encoding = "utf-8"
            global state
            state = re.status_code
            # print(state)
        except (ValueError, ConnectionError, requests.HTTPError, requests.Timeout, requests.TooManyRedirects) as e:
            state = 404
            logging.exception(e)
            self.warning.emit("网络连接错误")
        while True:
            if state == 200:
                # 将每个摄像头信息传入tegu进行监测
                global cam_id, warning_cam
                warning_cam = ""
                for cam_id in range(10):
                    # print(cam_id)
                    # 用post方法将缓存图片传入tegu
                    r = requests.post(r"http://127.0.0.1:8888/upload_to_tegu")
                    # print(r.status_code)
                    # 获得json文件然后读取
                    info = json.loads(r.content)
                    # print(info)
                    # 判断返回情况只有晚上才开始判断,将返回的嵌套列表flatten然后查看是否含有元素
                    if humanWarning in list(chain.from_iterable(info)) and (
                            int(time.strftime("%H")) >= 22 or int(time.strftime("%H")) <= 7):
                        warning_cam = warning_cam + "警告，摄像头"+str(cam_id)+"发现有人出没\n"
                    elif hydrantWarning in list(chain.from_iterable(info)):
                        warning_cam = warning_cam + "警告，摄像头" + str(cam_id) + "发现消防器材被移动\n"
                if warning_cam is not None:
                    self.warning.emit(warning_cam)
                else:
                    self.warning.emit("正常")
            else:
                self.warning.emit("网络连接错误")
                # SleepTime秒后进行监测
            time.sleep(sleepTime)
    '''
    # 将返回的信号进行检验
    def run(self):
        # 定义视频信号源
        getNVR.define_captures()
        while True:
            # 将每个摄像头信息传入tegu进行监测
            global cam_id, warning_message
            warning_message = ""
            for cam_id, cam_capture in getNVR.captures:
                # print(cam_id)
                # 判断摄像头是否正常工作
                if cam_capture is not None:
                    # 生成缓存文件以监测
                    getNVR.make_cache(cam_capture)
                    try:
                        # 用post方法将缓存图片传入tegu
                        global r
                        r = requests.post(r"http://127.0.0.1:8888/upload_to_tegu", files={'file': (r'cache.png', open(
                                    'cache.png', 'rb'), 'image/png', {})})
                        r.encoding = "utf-8"
                        # 获得json文件然后读取
                        global info
                        info = json.loads(r.content)
                        # 判断返回情况并且只有晚上才开始判断,将返回的嵌套列表flatten然后查看是否含有元素
                        if humanWarning in list(chain.from_iterable(info)) and (
                                int(time.strftime("%H")) >= 22 or int(time.strftime("%H")) <= 7):
                            warning_message = warning_message + "警告，摄像头" + str(cam_id) + "发现有人出没\n"
                        elif hydrantWarning in list(chain.from_iterable(info)):
                            warning_message = warning_message + "警告，摄像头" + str(cam_id) + "发现消防器材被移动\n"
                    except(ValueError,
                           ConnectionError, requests.HTTPError, requests.Timeout, requests.TooManyRedirects) as e:
                        # 错误处理
                        logging.exception(e)
                        warning_message = warning_message + "摄像头" + str(cam_id) + "连接错误\n"
                        # print(r.status_code)
                else:
                    # 空摄像头处理
                    warning_message = warning_message + "摄像头" + str(cam_id) + "无法获取\n"
            if warning_message is not None:
                self.warning.emit(warning_message)
            else:
                self.warning.emit("正常")
            # sleepTime秒后再次执行
            time.sleep(sleepTime)


if __name__ == "__main__":
    pygame.mixer.init()
    pygame.mixer.music.load(file)
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
