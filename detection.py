import cv2
import numpy as np
import configparser
from getNVR import hydrant_hog

# 火焰的RGB范围
lower = np.array([18, 50, 50], dtype="uint8")
upper = np.array([35, 255, 255], dtype="uint8")
conf = configparser.ConfigParser()
conf.read("config.ini")
fire_threshold = int(conf["NOUN"]["fire_threshold"])  # 火焰判断阈值
hydrant_threshold = int(conf["NOUN"]["hydrant_threshold"])   # 消防栓HOG阈值
cap_location = conf["LOCATION"]["cap_location"].split(",")  # 摄像头地点
hydrant_location = conf["LOCATION"]["hydrant_location"].split(",")  # 消防栓所在地


# 读取并生成cache文件并监测有没有火灾
def make_cache(capture, cam_id):
    if not (isinstance(capture, cv2.VideoCapture) or capture is None):
        #  参数类型检查
        raise TypeError('bad operand type')
    rval, frame = capture.read()
    message = ""
    if rval:
        cv2.imwrite('cache.jpg', frame)
        # cv2.imread(frame)
        if fire_detective(frame):
            message = message + "fire"
        # 计算并比对HOG特征
        cap_hog = hydrant_detective(frame, cam_id)
        location = cap_location[cam_id]
        hog_num = hydrant_location.index(location)
        compare_hog = hydrant_hog[hog_num]
        different = np.linalg.norm(cap_hog - compare_hog, ord=2)
        if different < hydrant_threshold:
            message = message + "hydrant"
        cv2.waitKey(5)
        capture.release()
        return message
    else:
        message = "error"
        return message


# 展现当前的监控图片（以后可能改成视频）
def show_cap():
    cache_pic = cv2.imread("cache.jpg")
    cv2.imshow("警告！", cache_pic)


# 用HOG特征匹配判断是否有人动了消防栓
def hydrant_detective(frame, cam_id):
    # 根据位置不同标注不同的
    if cam_id == 0:
        # 老图书馆3F-1
        x1 = 1125
        x2 = 1210
        y1 = 225
        y2 = 440
        hydrant = frame[y1:y2, x1:x2]
        hog = cv2.HOGDescriptor()
        h = hog.compute(hydrant)
        h = h.flatten()
        return h
    elif cam_id == 3:
        # 老图书馆3F-4
        x1 = 1120
        x2 = 1170
        y1 = 90
        y2 = 130
        hydrant = frame[y1:y2, x1:x2]
        hog = cv2.HOGDescriptor()
        h = hog.compute(hydrant)
        h = h.flatten()
        return h
    elif cam_id == 8:
        # 老图书馆3F-9
        x1 = 995
        x2 = 1048
        y1 = 330
        y2 = 408
        hydrant = frame[y1:y2, x1:x2]
        hog = cv2.HOGDescriptor()
        h = hog.compute(hydrant)
        return h
    elif cam_id == 12:
        # 老图书馆4F-3
        x1 = 135
        x2 = 240
        y1 = 675
        y2 = 870
        hydrant = frame[y1:y2, x1:x2]
        hog = cv2.HOGDescriptor()
        h = hog.compute(hydrant)
        return h
    else:
        return False


# 用高斯滤波过滤提取可能的火焰像素，原图片为1920*1080 = 2073600
def fire_detective(frame):
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    # output = cv2.bitwise_and(frame, hsv, mask=mask)
    # cv2.imshow("output", output)
    no_red = cv2.countNonZero(mask)
    print("output:", frame)
    if int(no_red) > fire_threshold:
        return True
    else:
        return False
