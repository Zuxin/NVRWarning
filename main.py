import sys
import requests
import time
import pygame
import json
import logging
import getNVR
import detection
import configparser
from itertools import chain
from PyQt5.QtWidgets import QApplication, QMainWindow
from firstMainWin import Ui_mainWindow
from PyQt5.QtCore import QTimer, QDateTime, pyqtSignal, QThread


def console_out(log_filename):
    # 定义一个Handler
    logging.basicConfig(
        level=logging.DEBUG,  # 定义输出到文件的log级别，
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
        datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
        filename=log_filename,  # log文件名
        filemode='a')  # 写入模式“w”或“a”
    # 定义Handler
    console = logging.StreamHandler()  # 定义console handler
    console.setLevel(logging.INFO)  # 定义该handler级别
    formatter = logging.Formatter(
        '%(asctime)s  %(filename)s : %(levelname)s  %(message)s'
    )  # 定义该handler格式
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)  # 实例化添加handler
    '''
    # 输出日志级别
    logging.debug('logger debug message')
    logging.info('logger info message')
    logging.warning('logger warning message')
    logging.error('logger error message')
    '''


class MyMainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置定时器将定时器的信号与槽链接
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        # 设置时间间隔并启动
        self.timer.start(1000)
        # 设置显示当前ip
        self.show_ip()
        self.init_ui()

    def init_ui(self):
        # 创建线程
        self.backend = BackendThread()
        # 连接信号
        self.backend.warning.connect(self.show_message)
        # 开始线程
        self.backend.start()

    # 显示当前ip地址
    def show_ip(self):
        self.label_4.setText("当前ip:\n" + tegu_ip)

    # 显示时间
    def show_time(self):
        time = QDateTime.currentDateTime()
        time_display = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.label_3.setText(time_display)

    # 警告信息
    def show_message(self, message):
        print("警告是"+message)
        if message == "正常":
            self.label.setText("正常")
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
            # detection.show_cap()
        else:
            self.label.setText(message)
            self.setStyleSheet('''
            #label { color: orange }
                                    ''')


# 子线程处理后台逻辑防止堵塞
class BackendThread(QThread):
    # 通过类成员定义信号
    warning = pyqtSignal(str)

    # 将返回的信号进行检验
    def run(self):
        # 定义视频信号源
        try:
            # 初始化
            getNVR.define_captures()
            getNVR.define_hydrant()
            time.sleep(1)
            getNVR.init_differents()
        except Exception as e:
            logging.warning(e)
            raise e
        while True:
            try:
                global warning_message
                warning_message = ""
                # 将每个摄像头信息传入Tegu/传统方法进行监测
                for cam_capture in getNVR.captureList:
                    # 判断摄像头是否正常工作
                    if cam_capture is not None:
                        global cam_id, location
                        cam_id = getNVR.captureList.index(cam_capture)
                        print("第"+str(cam_id)+"号摄像头正在检测")
                        temporary_message = detection.make_cache(cam_capture, cam_id)
                        location = cap_location[cam_id]
                        if "error" not in temporary_message:
                            if "fire" in temporary_message:
                                warning_message = warning_message + "警告,摄像头"+location+"处发现火灾\n"
                                detection.show_cap(cam_capture)
                            if "hydrant" in temporary_message:
                                warning_message = warning_message + "警告,摄像头"+location+"处可能有人移动消防栓\n"
                                detection.show_cap(cam_capture)
                            try:
                                # 用post方法将缓存图片传入tegu
                                global r
                                r = requests.post(
                                    r"http://127.0.0.1:8888/upload_to_tegu",
                                    files={
                                        'file': (r'cache.jpg',
                                                 open('cache.jpg', 'rb'),
                                                 'image/png', {})
                                    })
                                r.encoding = "utf-8"
                                # 获得json文件然后读取
                                global info
                                info = json.loads(r.content)
                                # print(info)
                                # 判断返回情况并且只有晚上才开始判断,将返回的嵌套列表flatten然后查看是否含有元素
                                resualt = list(chain.from_iterable(info))

                                if humanWarning in resualt and (
                                            int(time.strftime("%H")) >= 22
                                            or int(time.strftime("%H")) <= 7):
                                    humanumber = resualt.index(humanWarning)
                                    print("人类置信度"+resualt[humanumber+1])
                                    if float(resualt[humanumber+1]) > 1:
                                        warning_message = (
                                            warning_message + "警告，摄像头" + location + "发现有人出没\n")
                                        detection.show_cap(cam_capture)
                            except (ValueError, ConnectionError, FileNotFoundError,
                                    requests.HTTPError, requests.Timeout,
                                    requests.TooManyRedirects) as e:
                                # 错误处理
                                logging.error(e)
                                logging.exception(e)
                                warning_message = warning_message + "摄像头" + "连接错误\n"
                                print(r.status_code)
                        else:
                            warning_message = warning_message + "摄像头"+str(cam_id)+"读取错误\n"
                            for i in getNVR.captureList:
                                i.release()
                            getNVR.captureList = []
                            getNVR.define_captures()
                    else:
                        # 空摄像头处理
                        print("错误")
                        warning_message = warning_message + "摄像头" + "无法获取\n"
                    print(warning_message)
                    if warning_message:
                        self.warning.emit(warning_message)
                    else:
                        self.warning.emit("正常")
                # sleepTime秒后再次执行
                time.sleep(int(sleepTime))
            except Exception as e:
                logging.critical(e)
                for i in getNVR.captureList:
                    i.release()
                getNVR.captureList = []
                getNVR.define_captures()


if __name__ == "__main__":
    # 读取配置文件
    conf = configparser.ConfigParser()
    conf.read("config.ini")
    tegu_ip = conf["HOST_IP"]["ip"]
    url = r"http://" + tegu_ip + ":8888/upload_to_tegu"  # 连接tegu
    humanWarning = conf["WARNING"]["humanWarning"]  # 出现人的警告信息
    hydrantWarning = conf["WARNING"]["hydrantWarning"]  # 消防设备警告信息
    FireWarning = conf["WARNING"]["fireWarning"]  # 火灾警告信息
    sleepTime = conf["NOUN"]["sleep_time"]  # 每次取视频的循环间隔时间
    warning_sound = conf["FILE"]["warning_sound"]  # 警报音
    cap_location = conf["LOCATION"]["cap_location"].split(",")  # 摄像头地点
    # 读取报警音效
    pygame.mixer.init()
    pygame.mixer.music.load(warning_sound)
    # 设置log日志
    console_out('logging.log')

    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    qssStyle = '''
    #label { color: orange;
    }
    #label_3 { color: blue
    }
    #label_4 { color: green
    }
        '''
    myWin.setStyleSheet(qssStyle)
    myWin.show()
    sys.exit(app.exec_())
