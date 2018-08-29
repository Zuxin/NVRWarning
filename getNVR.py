import cv2
import requests
from PIL import Image


# 摄像头列表
# 正常是26-43 是学校的摄像头不过有一些不能用
cameraList = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43]
# 每次取视频的循环间隔时间
sleepTime = 10
# 是否开始检测
isStarted = False
# 摄像头信号源列表
captures = []

# 定义视频信号源
for i in cameraList:
    vc = cv2.VideoCapture('rtsp://admin:Ccut@edu2017@10.205.12.' + str(i) + ':554/Streaming/Channels/101?transportmode=unicast')
    # print(vc.isOpened())
    if vc.isOpened():
        captures.append(vc)
    else:
        del cameraList[i]


# 将摄像头信号送入后端
def input_video_capture():
    pass