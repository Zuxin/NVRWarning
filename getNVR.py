import cv2
import time
import requests

# 图像传入地址
url = r"http://127.0.0.1:8888/upload_to_tegu"
# 上传用缓存文件
files = {'file': (r'cache.png', open('cache.png', 'rb'), 'image/png', {})}
# 摄像头列表 正常是26-43 是学校的摄像头可能有一些不能用
cameraList = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43]
# 每次取视频的循环间隔时间
sleepTime = 10
# 摄像头信号源列表
captures = []


# 定义视频信号源
def define_captures():
    for i in cameraList:
        cap = cv2.VideoCapture('rtsp://admin:Ccut@edu2017@10.205.12.' + str(i) + ':554/Streaming/Channels/101?transportmode=unicast')
        # print(vc.isOpened())
        # 检测摄像头是否能用并添加进列表
        if cap.isOpened():
            captures.append(cap)
        else:
            del cameraList[i]


# 将摄像头信号送入后端
def input_video_capture(isStarted):
    while isStarted:
        for j in captures:
            try:
                rval, frame = j.read()
                cv2.imwrite('cache.png', frame)
                cv2.waitKey(1)
                r = requests.post(url, files=files)
                print(r.text)
            except:
                print("第" + str(captures.index(j)) + "个摄像头发生错误")
        time.sleep(sleepTime)

