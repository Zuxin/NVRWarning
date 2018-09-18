# pylint: disable=no-member
import cv2


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
# 摄像头信号源列表
captureList = []
# captures = {}


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


# 读取并生成cache文件


def make_cache(cam_capture):
    if not isinstance(cam_capture, (cv2.VideoCapture, None)):
        #  参数类型检查
        raise TypeError('bad operand type')
    rval, frame = cam_capture.read()
    cv2.imwrite('cache.png', frame)
    # cv2.imread(frame)
    '''
    if rval:
        #  检查是否正常输出
        pass
    '''
    return rval
    cv2.release(cam_capture)
    cv2.waitKey(10)
