import cv2
import numpy as np

img1 = cv2.imread('Bird1.jpg')
img2 = cv2.imread('Bird2.jpg')

img_stack = np.hstack((img1,img2))

cv2.imshow('Image Stack',img_stack)
cv2.waitKey(0)
cv2.destroyAllWindows()
