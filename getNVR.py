# pylint: disable=no-member
import cv2
import numpy as np
import configparser
from skimage import feature as ft
# from HOGcompute import Hog_descriptor
conf = configparser.ConfigParser()
conf.read("config.ini")
# 摄像头列表 正常是26-43 是学校的摄像头可能有一些不能用
cameraList = conf["HOST_IP"]["cameraList"].split(",")
# 摄像头信号源列表
captureList = []
# 初始帧做背景参考
pre_frame = []
'''
# 消防栓HOG特征
hydrant_hogs = []
initial_hog_differents = []
'''


# 定义视频信号源
def define_captures():
    for i in cameraList:
        # 经过RTSP协议获得摄像数据
        print("第"+str(i)+"号摄像头检测")
        try:
            cap = cv2.VideoCapture(
                'rtsp://admin:Ccut@edu2017@10.205.12.' + i +
                ':554/Streaming/Channels/101?transportmode=unicast')
            # print(cap.isOpened())
            if cap.isOpened():
                captureList.append(cap)
            else:
                captureList.append(None)
        except Exception:
            print('第' + i + "号摄像头存在问题")
        # 检测摄像头是否能用并添加进列表

'''
# 生成消防栓的特征
def define_hydrant():
    # hog = cv2.HOGDescriptor()
    print("开始检测")
    for i in captureList:
        hyd_id = captureList.index(i)
        print(hyd_id)
        if hyd_id == 0:
            # 老图书馆3F-1
            rval, frame = i.read()
            if rval:
                bbox = (1120,225,100,215)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                hydrant_hogs.append(frame)
                print("摄像头1"+str(frame))
            else:
                print("摄像头1存在问题")
        elif hyd_id == 3:
            # 老图书馆3F-4
            rval, frame = i.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            if rval:
                bbox = (1110,70,77,70)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                hydrant_hogs.append(frame)
                print("摄像头2"+str(frame))
            else:
                print("摄像头2存在问题")
        elif hyd_id == 6:
            # 老图书馆3F-7
            rval, frame = i.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            if rval:
                bbox = (1512, 807, 100, 153)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                hydrant_hogs.append(frame)
                print("摄像头3"+str(frame))
            else:
                print("摄像头3存在问题")
        elif hyd_id == 8:
            # 老图书馆3F-9
            rval, frame = i.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            if rval:
                bbox = (1011, 327, 33, 88)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                hydrant_hogs.append(frame)
                print("摄像头4"+str(frame))
            else:
                print("摄像头4存在问题")
        elif hyd_id == 12:
            # 老图书馆4F-3
            rval, frame = i.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            if rval:
                bbox = (137, 679, 145, 171)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                hydrant_hogs.append(frame)
                print("摄像头5"+str(frame))
            else:
                print("摄像头5存在问题")
                
                
def init_differents():
    # hog = cv2.HOGDescriptor()
    print("开始检测")
    for i in captureList:
        hyd_id = captureList.index(i)
        print(hyd_id)
        if hyd_id == 0:
            # 老图书馆3F-1
            rval, frame = i.read()
            if rval:
                bbox = (1120,225,100,215)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                compare_hog = hydrant_hogs[0]
                different = np.sqrt(np.sum(np.square(frame - compare_hog)))
                initial_hog_differents.append(different)
                print("初始差异值1"+str(different))
            else:
                print("摄像头1存在问题")
        elif hyd_id == 3:
            # 老图书馆3F-4
            rval, frame = i.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            if rval:
                bbox = (1110,70,77,70)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                compare_hog = hydrant_hogs[1]
                different = np.sqrt(np.sum(np.square(frame - compare_hog)))
                initial_hog_differents.append(different)
                print("初始差异值2"+str(different))
            else:
                print("摄像头2存在问题")
        elif hyd_id == 6:
            # 老图书馆3F-7
            rval, frame = i.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            if rval:
                bbox = (1512, 807, 100, 153)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                compare_hog = hydrant_hogs[2]
                different = np.sqrt(np.sum(np.square(frame - compare_hog)))
                initial_hog_differents.append(different)
                print("初始差异值3"+str(different))
            else:
                print("摄像头3存在问题")
        elif hyd_id == 8:
            # 老图书馆3F-9
            rval, frame = i.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            if rval:
                bbox = (1011, 327, 33, 88)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                compare_hog = hydrant_hogs[3]
                different = np.sqrt(np.sum(np.square(frame - compare_hog)))
                initial_hog_differents.append(different)
                print("初始差异值4"+str(different))
            else:
                print("摄像头4存在问题")
        elif hyd_id == 12:
            # 老图书馆4F-3
            rval, frame = i.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            if rval:
                bbox = (137, 679, 145, 171)
                frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
                #hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
                # vector, image = hog.extract()
                # print (np.array(vector))
                frame = ft.hog(frame,visualise=False)
                frame  = frame.ravel()
                np.float32(frame)
                compare_hog = hydrant_hogs[4]
                different = np.sqrt(np.sum(np.square(frame - compare_hog)))
                initial_hog_differents.append(different)
                print("初始差异值5"+str(different))
            else:
                print("摄像头5存在问题")
'''


# 生成消防栓的特征
def define_hydrant():
    for i in captureList:
        hyd_id = captureList.index(i)
        print(hyd_id)
        bbox = []
        if hyd_id == 0:
            # 老图书馆3F-1
            bbox = [1120, 225, 100, 215]
        elif hyd_id == 3:
            # 老图书馆3F-4
            bbox = [1110, 70, 77, 70]
        elif hyd_id == 6:
            # 老图书馆3F-7
            bbox = [1512, 807, 100, 153]
        elif hyd_id == 8:
            # 老图书馆3F-9
            bbox = [1011, 327, 33, 88]
        elif hyd_id == 12:
            # 老图书馆4F-3
            bbox = [137, 679, 145, 171]
        if bbox:
            rval, frame = i.read()
            frame = frame[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])]
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_img = cv2.resize(gray_img, (500, 500))
            gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)
            pre_frame.append(gray_img)

