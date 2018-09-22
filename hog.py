import cv2


# 用HOG特征匹配判断是否有人动了消防栓
def compute_hog(cam_capture, cam_id):
    # 根据位置不同标注不同的
    if cam_id == 0:
        # 老图书馆3F-1
        x1 = 1125
        x2 = 1210
        y1 = 225
        y2 = 440
        rval, frame = cam_capture.read()
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
        rval, frame = cam_capture.read()
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
        rval, frame = cam_capture.read()
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
        rval, frame = cam_capture.read()
        hydrant = frame[y1:y2, x1:x2]
        hog = cv2.HOGDescriptor()
        h = hog.compute(hydrant)
        return h

