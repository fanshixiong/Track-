from skimage.measure import compare_ssim as ssim
import imutils
import cv2

class Detect:
    def __init__(self, ratio):
        self.ratio = ratio

    def initDetect(self, gray1, gray2):
        # 计算两个灰度图像之间的相似度
        (score, diff) = ssim(gray1, gray2, full=True)
        diff = (diff * 255).astype("uint8")
        hit = False
        boundingbox = list()
        if (score < self.ratio):
            thresh = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY_INV)[1]
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[1] if imutils.is_cv3() else cnts[0]
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                if (w < 70 or h < 20):
                    continue
                else:
                    boundingbox = list([x, y, w, h])
                    hit = True
                    break
        return hit, boundingbox


    def onDetect(self, gray1, gray2):
        (score, diff) = ssim(gray1, gray2, full=True)
        hit = True
        if (score >= self.ratio):
            hit = False
        return hit



