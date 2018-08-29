import sys
import requests
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QDialog
from firstMainWin import Ui_mainWindow
from PyQt5.QtCore import QTimer, QDateTime, pyqtSignal, QThread


url = "http://bbs.ngacn.cc"   # 测试用地址
humanWarning = ""  # 出现人的警告信息
hydrantWarning = ""  # 消防设备警告信息


class MyMainWindow(QMainWindow, Ui_mainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        '''
        # 子窗口
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        '''
        # 设置定时器将定时器的信号与槽链接
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        # 设置时间间隔并启动
        self.timer.start(1000)
        self.init_ui()

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
        if data == "摄像头监测到有人出没" or "摄像头检测到消防设备被移动":
            self.setStyleSheet('''
            #label { color: red }
                                    ''')
        elif data == "网络错误请检查网络":
            self.setStyleSheet('''
            #label { color: orange }
                                    ''')
        elif data == "正常":
            self.setStyleSheet('''
                #label { color: green; 
                }
                ''')
        self.label.setText(data)


class BackendThread(QThread):
    # 通过类成员定义信号
    warning = pyqtSignal(str)
    # 处理逻辑

    def run(self):
        while True:
            try:
                r = requests.get(url)
                r.encoding = "utf-8"
                state = r.status_code
            except:
                state = "404"
            if state == 200:
                # print("连接成功"+str(state))
                # 暂定
                if r.text == humanWarning:
                    self.warning.emit("摄像头监测到有人出没")
                elif r.text == hydrantWarning:
                    self.warning.emit("摄像头检测到消防设备被移动")
                else:
                    self.warning.emit("正常")
            else:
                # print("连接失败"+str(state))
                self.warning.emit("网络错误请检查网络")
            time.sleep(1)


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
