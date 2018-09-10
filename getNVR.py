import cv2


# 摄像头列表 正常是26-43 是学校的摄像头可能有一些不能用
cameraList = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43]
# 摄像头信号源列表
captureList = []
captures = {}


# 定义视频信号源
def define_captures():
    for i in cameraList:
        # 经过RTSP协议获得摄像数据
        cap = cv2.VideoCapture('rtsp://admin:Ccut@edu2017@10.205.12.' + str(i) +
                               ':554/Streaming/Channels/101?transportmode=unicast')
        # print(cap.isOpened())
        # 检测摄像头是否能用并添加进列表
        if cap.isOpened():
            captureList.append(cap)
        else:
            captureList.append(None)
        print(cap)
    global captures
    captures = dict(zip(cameraList, captureList))


# 读取并生成cache文件
def make_cache(cam_capture):
    if not isinstance(cam_capture, cv2.VideoCapture):
        #  参数类型检查
        raise TypeError('bad operand type')
    rval, frame = cam_capture.read()
    cv2.imwrite('cache.png', frame)
    if not rval:
        #  检查是否正常输出
        raise TypeError('bad operand type')
    cv2.waitKey(1)

