# pylint: disable=no-member
import cv2

'''
这一部分以后可以写在txt里
'''
# 摄像头列表 正常是26-43 是学校的摄像头可能有一些不能用
cameraList = [
    "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
    "39", "40", "41", "42", "43"
]
# 摄像头对应的地点
cap_location = [
    "老图书馆3F-1", "老图书馆3F-2", "老图书馆3F-3", "老图书馆3F-4", "老图书馆3F-5", "老图书馆3F-6",
    "老图书馆3F-7", "老图书馆3F-8", "老图书馆3F-9", "老图书馆3F-9", "老图书馆3F-10", "老图书馆3F-11",
    "老图书馆4F-1", "老图书馆4F-3", "老图书馆4F-4", "老图书馆4F-5", "老图书馆4F-6", "老图书馆4F-7"
]
# 有消防拴的地点
hydrant_location = ["老图书馆3F-1", "老图书馆3F-4", "老图书馆3F-7", "老图书馆3F-9", "老图书馆4F-3"]
# 摄像头信号源列表
captureList = []
# 消防栓HOG特征
hydrant_hog = []


# 定义视频信号源
def define_captures():
    for i in cameraList:
        # 经过RTSP协议获得摄像数据
        # print("第"+str(i)+"号摄像头检测")
        try:
            cap = cv2.VideoCapture(
                'rtsp://admin:Ccut@edu2017@10.205.12.' + i +
                ':554/Streaming/Channels/101?transportmode=unicast')
        except Exception:
            print(str(i) + "号摄像头存在问题")
        # 检测摄像头是否能用并添加进列表
        print(cap.isOpened())
        if cap.isOpened():
            captureList.append(cap)
        else:
            captureList.append(None)


# 生成消防栓的特征
def define_hydrant():
    for i in captureList:
        hyd_id = captureList.index(i)
        if hyd_id == 0:
            # 老图书馆3F-1
            rval, frame = i.read()
            x1 = 1120
            x2 = 1170
            y1 = 90
            y2 = 130
            hydrant = frame[y1:y2, x1:x2]
            hog = cv2.HOGDescriptor()
            h = hog.compute(hydrant)
            h = h.flatten()
            # print("第"str(hyd_id)+"个HOG:"+str(i))
            hydrant_hog.append(h)
        elif hyd_id == 3:
            # 老图书馆3F-4
            rval, frame = i.read()
            x1 = 1113
            x2 = 1182
            y1 = 80
            y2 = 144
            hydrant = frame[y1:y2, x1:x2]
            hog = cv2.HOGDescriptor()
            h = hog.compute(hydrant)
            h = h.flatten()
            hydrant_hog.append(h)
            # print("第"str(hyd_id)+"个HOG:"+str(i))
        elif hyd_id == 6:
            # 老图书馆3F-7
            rval, frame = i.read()
            x1 = 1504
            x2 = 1590
            y1 = 825
            y2 = 958
            hydrant = frame[y1:y2, x1:x2]
            hog = cv2.HOGDescriptor()
            h = hog.compute(hydrant)
            h = h.flatten()
            hydrant_hog.append(h)
            # print("第"str(hyd_id)+"个HOG:"+str(i))
        elif hyd_id == 8:
            # 老图书馆3F-9
            rval, frame = i.read()
            x1 = 995
            x2 = 1048
            y1 = 330
            y2 = 408
            hydrant = frame[y1:y2, x1:x2]
            hog = cv2.HOGDescriptor()
            h = hog.compute(hydrant)
            h = h.flatten()
            hydrant_hog.append(h)
            # print("第"str(hyd_id)+"个HOG:"+str(i))
        elif hyd_id == 12:
            # 老图书馆4F-3
            rval, frame = i.read()
            x1 = 135
            x2 = 240
            y1 = 675
            y2 = 870
            hydrant = frame[y1:y2, x1:x2]
            hog = cv2.HOGDescriptor()
            h = hog.compute(hydrant)
            h = h.flatten()
            hydrant_hog.append(h)
            # print("第"str(hyd_id)+"个HOG:"+str(i))


# 读取并生成cache文件
def make_cache(cam_capture):
    if not (isinstance(cam_capture, cv2.VideoCapture) or cam_capture is None):
        #  参数类型检查
        raise TypeError('bad operand type')
    rval, frame = cam_capture.read()
    cv2.imwrite('cache.jpg', frame)
    # cv2.imread(frame)
    if not rval:
        #  检查是否正常输出
        cam_capture.release()
    cv2.waitKey(500)
    return rval


# 展现当前的监控图片（以后改成视频）
def show_cap(cam_capture):
    if not (isinstance(cam_capture, cv2.VideoCapture) or cam_capture is None):
        #  参数类型检查
        raise TypeError('bad operand type')
    cv2.imshow("cache.jpg")


