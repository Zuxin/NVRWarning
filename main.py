import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QDialog
from firstMainWin import Ui_mainWindow
from PyQt5.QtCore import QTimer, QDateTime, pyqtSignal, QThread


class MyMainWindow(QMainWindow, Ui_mainWindow):
    url = "www.weather0.com"   # 测试用地址
    humanWarning = ""  # 出现人的警告信息
    hydrantWarning = ""  # 消防设备警告信息

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
        self.timer.timeout.connect(self.show_message)
        # 设置时间间隔并启动
        self.timer.start(1000)
    # 显示时间

    def show_time(self):
        time = QDateTime.currentDateTime()
        time_dsplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.label_3.setText(time_dsplay)
    # 判断并显示警告信息

    def show_message(self):
        self.show_time()
        global r
        try:
            r = requests.get(self.url)
            r.encoding = "utf-8"
            state = r.status_code
        except:
            state = "404"
        if state == 200:
            # print("连接成功")
            # 暂定
            if r.text == self.humanWarning:
                self.label.setText("摄像头监测到有人出没")
                self.setStyleSheet('''
                        #label { color: red }
                        ''')
                '''
                sub = QMainWindow()
                sub.setWidget(QDialog())
                sub.setWindowTitle("警告！")
                sub.show()
                '''
            elif r.text == self.hydrantWarning:
                self.setStyleSheet('''
                        #label { color: red }
                        ''')
                self.label.setText("摄像头检测到消防设备被移动")
                '''
                sub = QMainWindow()
                sub.setWidget(QDialog())
                sub.setWindowTitle("警告！")
                sub.show()
                '''
        else:
            # print("连接失败")
            self.setStyleSheet('''
                        #label { color: orange }
                        ''')
            self.label.setText("网络错误请检查网络")


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
