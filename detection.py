import cv2
import numpy as np
import configparser
# from getNVR import hydrant_hogs, initial_hog_differents
# from skimage import feature as ft
from getNVR import pre_frame


# 火焰的RGB范围
redThre = 115
saturationTh = 45
'''
lower = np.array([18, 50, 50], dtype="uint8")
upper = np.array([35, 255, 255], dtype="uint8")
'''
conf = configparser.ConfigParser()
conf.read("config.ini")
fire_threshold = float(conf["NOUN"]["fire_threshold"])  # 火焰判断阈值
hydrant_threshold = float(conf["NOUN"]["hydrant_threshold"])   # 消防栓HOG阈值
cap_location = conf["LOCATION"]["cap_location"].split(",")  # 摄像头地点
hydrant_location = conf["LOCATION"]["hydrant_location"].split(",")  # 消防栓所在地


# 读取并生成cache文件并监测有没有火灾
def make_cache(capture, cam_id):
    if not (isinstance(capture, cv2.VideoCapture) or capture is None):
        #  参数类型检查
        raise TypeError('bad operand type')
    rval, frame = capture.read()
    fire_message = ""
    if rval:
        cv2.imwrite('cache.jpg', frame)
        # cv2.imread(frame)
        if fire_detective(frame):
            fire_message = fire_message + "fire"
        '''
        # 计算并比对HOG特征
        if cam_id in [0, 3, 6, 8, 12]:
            cap_hog = hydrant_detective(frame, cam_id)
            hog_num = [0, 3, 6, 8, 12].index(cam_id)
            print("hognum："+str(hog_num))
            compare_hog = hydrant_hogs[hog_num]
            if compare_hog.any():
                different = np.sqrt(np.sum(np.square(cap_hog - compare_hog)))
                print("差异第"+str(hog_num)+"个数值为"+str(different))
                print("消防栓比对差异:"+hydrant_location[hog_num]+"="+str(different - initial_hog_differents[hog_num]))
                if abs(different - initial_hog_differents[hog_num]) > hydrant_threshold:
                    fire_message = fire_message + "hydrant"
        '''
        if hydrant_detective(frame, cam_id):
            fire_message = fire_message + "hydrant"
        return fire_message
    else:
        fire_message = "error"
        return fire_message
    cv2.waitKey(60)


# 展现当前的监控图片（以后可能改成视频）
def show_cap(capture):
    # cv2.namedWindow("Warning",0)
    # cv2.resizeWindow("Warning", 640, 480)
    rval, frame = capture.read()
    cv2.imshow("Warning", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


'''
# 用HOG特征匹配判断是否有人动了消防栓
def hydrant_detective(frame, cam_id):
    if cam_id == 0:
        # 老图书馆3F-1
        bbox = (1120, 225, 100, 215)
        frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
        # hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
        # vector, image = hog.extract()
        # print (np.array(vector))
        frame = ft.hog(frame, visualise=False)
        frame  = frame.ravel()
        return frame
    elif cam_id == 3:
        # 老图书馆3F-4
        bbox = (1110, 70, 77, 70)
        frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
        # hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
        # vector, image = hog.extract()
        # print (np.array(vector))
        frame = ft.hog(frame, visualise=False)
        frame  = frame.ravel()
        return frame
    elif cam_id == 6:
        # 老图书馆3F-7
        bbox = (1512, 807, 100, 153)
        frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
        # hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
        # vector, image = hog.extract()
        # print (np.array(vector))
        frame = ft.hog(frame, visualise=False)
        frame  = frame.ravel()
        return frame
    elif cam_id == 8:
        # 老图书馆3F-9
        bbox = (1011, 327, 33, 88)
        frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
        # hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
        # vector, image = hog.extract()
        # print (np.array(vector))
        frame = ft.hog(frame, visualise=False)
        frame  = frame.ravel()
        return frame
    elif cam_id == 12:
        # 老图书馆4F-3
        bbox = (137, 679, 145, 171)
        frame = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
        # hog = Hog_descriptor(frame, cell_size=8, bin_size=8)
        # vector, image = hog.extract()
        # print (np.array(vector))
        frame = ft.hog(frame, visualise=False)
        frame  = frame.ravel()
        return frame
    '''


'''
# 用高斯滤波过滤提取可能的火焰像素，原图片为1920*1080 = 2073600
def fire_detective(frame):
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    # output = cv2.bitwise_and(frame, hsv, mask=mask)
    # cv2.imshow("output", output)
    no_red = cv2.countNonZero(mask)
    print("火焰output:", no_red)
    sp = frame.shape
    if int(no_red)/(sp[0]*sp[1]) > fire_threshold:
        return True
    else:
        return False
'''


def hydrant_detective(frame, cam_id):
    # 选取范围和在相应list里的序号
    bbox = []
    hyd_id = 0
    different = 0
    if cam_id == 0:
        # 老图书馆3F-1
        bbox = [1120, 225, 100, 215]
        hyd_id = 0
    elif cam_id == 3:
        # 老图书馆3F-4
        bbox = [1110, 70, 77, 70]
        hyd_id = 1
    elif cam_id == 6:
        # 老图书馆3F-7
        bbox = [1512, 807, 100, 153]
        hyd_id = 2
    elif cam_id == 8:
        # 老图书馆3F-9
        bbox = [1011, 327, 33, 88]
        hyd_id = 3
    elif cam_id == 12:
        # 老图书馆4F-3
        bbox = [137, 679, 145, 171]
        hyd_id = 4
    frame = frame[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2])]
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.resize(gray_img, (500, 500))
    gray_img = cv2.GaussianBlur(gray_img, (21, 21), 0)
    compare_img = pre_frame[hyd_id]
    img_delta = cv2.absdiff(compare_img, gray_img)
    thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 1000:  # 敏感度
            continue
        else:
            different = different+1
    if different/len(contours) > hydrant_threshold:
        return True
    else:
        return False





def fire_detective(frame):
    B = frame[:, :, 0]
    G = frame[:, :, 1]
    R = frame[:, :, 2]
    minValue = np.array(np.where(R <= G, np.where(G <= B, R, np.where(R <= B, R, B)), np.where(G <= B, G, B)))
    S = 1 - 3.0 * minValue / (R + G + B + 1)
    fireImg = np.array(np.where(R > redThre, np.where(R >= G, np.where(G >= B, np.where(S >= 0.2, np.where(
        S >= (255 - R) * saturationTh / redThre, 255, 0), 0), 0), 0), 0))
    gray_fireImg = np.zeros([fireImg.shape[0], fireImg.shape[1], 1], np.uint8)
    gray_fireImg[:, :, 0] = fireImg
    gray_fireImg = cv2.GaussianBlur(gray_fireImg, (7, 7), 0)
    gray_fireImg = contrast_brightness(gray_fireImg, 5.0, 25)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    gray_fireImg = cv2.morphologyEx(gray_fireImg, cv2.MORPH_CLOSE, kernel)
    # dst = cv2.bitwise_and(frame, frame, mask=gray_fireImg)
    no_red = cv2.countNonZero(gray_fireImg)
    if no_red/(frame.shape[0]*frame.shape[1]) > fire_threshold:
        return True
    else:
        return False


def contrast_brightness(image, c, b):  # 其中c为对比度，b为每个像素加上的值（调节亮度）
    blank = np.zeros(image.shape, image.dtype)   # 创建一张与原图像大小及通道数都相同的黑色图像
    dst = cv2.addWeighted(image, c, blank, 1-c, b)   # c为加权值，b为每个像素所加的像素值
    ret, dst = cv2.threshold(dst, 25, 255, cv2.THRESH_BINARY)
    return dst




