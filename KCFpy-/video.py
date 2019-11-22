import cv2

class Video:
    def __init__(self, on, videopath):
        if (~on):
            self.cap = cv2.VideoCapture(videopath)
        else:
            self.cap = cv2.VideoCapture(videopath)
            #调用实时视频流


    def getVideo(self):
        return self.cap

