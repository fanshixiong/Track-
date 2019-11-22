import numpy as np 
import cv2
import sys
from time import time
import test
import imutils
import kcftracker
from skimage.metrics import structural_similarity
import text
import textgraph
#gui
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtMultimediaWidgets import QVideoWidget
from Gui import Ui_Tracker
from myVideoWidget import myVideoWidget
from mylabel import MyLabel
#import time
import winsound

class PlayMusic(object):
    """播放提示音乐"""
    def __init__(self, music, flag):
        self.music = music
        self.flag = flag

    def run(self):
        winsound.PlaySound(f'{self.music}', self.flag)


def play_music(music, flag, stop):
    #winsound.PlaySound('alert', winsound.SND_ASYNC)
    p1 = PlayMusic(music, flag)
    p1.run()

selectingObject = False
initTracking = False
onTracking = False
ix, iy, cx, cy = -1, -1, -1, -1
w, h = 0, 0
imt = 5

inteval = 1
class myMainWindow(Ui_Tracker, QMainWindow):
    def __init__(self):
        super(Ui_Tracker, self).__init__()
        self.setupUi(self)
        #self.initUI()

    def initUI(self):
        self.lb = MyLabel(self)  # 重定义的label
        print(self.lb.x0, self.lb.y0, self.lb.x1, self.lb.y1)

    def btn_Open_Clicked(self):
        self.filename,  _ = QFileDialog.getOpenFileName(self, '打开视频')
        if self.filename:
            self.cap=cv2.VideoCapture(self.filename)
        else:
            self.cap = cv2.VideoCapture(
                "rtsp://admin:WANG123456@192.168.43.249:554//CStreaminghannels/102?transportmode=unicast")
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rows, cols, channels = frame.shape
        bytesPerLine = channels * cols

        QImg = QImage(frame.data, cols, rows,
                          bytesPerLine, QImage.Format_RGB888)

        self.wgt_video.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.wgt_video.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    def btn_Play_Clicked(self):
        #if self.filename:
        #   self.cap = cv2.VideoCapture(self.filename)
        delay=30
        tracker = kcftracker.KCFTracker(True, True, True)  # hog, fixed_window, multiscale
        #tracker.setArea([400, 100, 700, 500])  # 监控范围 384 288
        tracker.setEntrance([198, 195, 51, 38])  # 设置入口
        tracker.setArea([self.wgt_video.x0+200, self.wgt_video.y0, abs(self.wgt_video.x1-self.wgt_video.x0)*2, abs(self.wgt_video.y1-self.wgt_video.y0)*2.5])
        a = textgraph._get_ground_truth('comroom2_055-239.txt')
        ground_truth = np.array(a)  # 标记数组
        positions = np.zeros([ground_truth.shape[0], ground_truth.shape[1]])
        print(self.wgt_video.x0+200, self.wgt_video.y0, abs(self.wgt_video.x1-self.wgt_video.x0)*2, abs(self.wgt_video.y1-self.wgt_video.y0)*2)
        i = 0

        while (self.cap.isOpened()):
            ret, frame1 = self.cap.read()
            i = i + 1
            if (i >= 3):
                break
        ret, frame1 = self.cap.read()
        i += 1
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        onTracking = False
        hit = False
        boundingbox = list()

        cnt = 0
        while (self.cap.isOpened()):
            ret, self.frame = self.cap.read()
            if not ret:
                break
            i += 1
            print(i)
            print(ret)
            gray2 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            # 计算两个灰度图像之间的相似度
            (score, diff) = structural_similarity(gray1, gray2, full=True)
            diff = (diff * 255).astype("uint8")
            #print("SSIM:{}".format(score))
            print(score)
            if (onTracking == False):
                if (score < 0.99):  # 差异性较大

                    thresh = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY_INV)[1]
                    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cnts = cnts[1] if imutils.is_cv3() else cnts[0]
                    # cv2.drawContours(frame1, cnts, -1 ,(0, 0, 255), 3)

                    for c in cnts:
                        (x, y, w, h) = cv2.boundingRect(c)
                        if (w < 70 or h < 20):
                            continue
                        else:
                            #print("x, y, w, h = ", (x,y,w,h))
                            boundingbox = list([x, y, w, h])
                            hit = True
                            break
                    if (hit):  # 检测到目标
                        cv2.rectangle(self.frame, (boundingbox[0], boundingbox[1]),
                                        (boundingbox[0] + boundingbox[2], boundingbox[1] + boundingbox[3]),
                                        (0, 0, 255), 1)
                        print("boundingbox = ", boundingbox)
                        tracker.init(boundingbox, self.frame)
                        onTracking = True
            elif (onTracking):
                if (score >= 0.99):  # 目标消失，停止更新
                    onTracking = False

                t0 = time()
                boundingbox, pvalue = tracker.update(self.frame)
                if (i >= 55 and i <= 239):
                    positions[i - 55] = np.array(boundingbox)
                    print(positions[i - 55])
                t1 = time()
                boundingbox = list(map(int, boundingbox))
                cv2.rectangle(self.frame, (boundingbox[0], boundingbox[1]),
                                (boundingbox[0] + boundingbox[2], boundingbox[1] + boundingbox[3]), (0, 255, 255), 1)
                if (tracker.monitoring()):  # 目标进入监控区域
                    fsize = boundingbox[2] // 6
                    #winsound.Beep(60, 10)
                    cnt += 1
                    if cnt >= imt:
                        play_music('msg.wav', winsound.SND_ALIAS, 2)
                    self.frame = textgraph.paint_chinese_opencv(self.frame, '进入监控区域',
                                                            (boundingbox[0], boundingbox[1] - fsize),
                                                            (255, 0, 0), fsize)
                duration = 0.01
                duration = 0.8 * duration + 0.2 * (t1 - t0)
                cv2.putText(self.frame, 'FPS: ' + str(1 / duration)[:4].strip('.') + '  pv = ' + str(pvalue), (8, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            if (delay >= 0 and cv2.waitKey(delay) >= 0):
                cv2.waitKey(0)
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            rows, cols, channels = self.frame.shape
            bytesPerLine = channels * cols

            QImg = QImage(self.frame.data, cols, rows,
                            bytesPerLine, QImage.Format_RGB888)
            #self.btn_Cap_Clicked()
            self.wgt_video.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.wgt_video.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        textgraph.show_precision(positions, ground_truth)

    def btn_Cap_Clicked(self):
        if not hasattr(self, "frame"):
            return
        self.captured = self.frame

        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        QImg = QImage(self.captured.data, cols, rows,
                    bytesPerLine, QImage.Format_RGB888)
        self.wgt_picture.setPixmap(QPixmap.fromImage(QImg).scaled(
                    self.wgt_picture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    def btn_Gray_Clicked(self):
        '''
        灰度化
        '''
        # 如果没有捕获图片，则不执行操作
        if not hasattr(self, "captured"):
            return
        self.captured = cv2.cvtColor(self.captured, cv2.COLOR_RGB2GRAY)

        rows, columns = self.captured.shape
        bytesPerLine = columns

        # 灰度图是单通道，所以需要用Format_Indexed8
        QImg = QImage(self.captured.data, columns, rows,
                      bytesPerLine, QImage.Format_Indexed8)
        self.wgt_gray.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.wgt_gray.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == '__main__':
    #gui
    app = QApplication(sys.argv)
    vieo_gui = myMainWindow()
    vieo_gui.show()
    sys.exit(app.exec_())