import numpy as np
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.pyplot as plt

def paint_chinese_opencv(im,chinese,pos,color,fsize):
	img_PIL = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))

	fillColor = color
	position = pos
	font = ImageFont.truetype('STXINWEI.TTF', fsize, encoding = 'utf-8')
	draw = ImageDraw.Draw(img_PIL)
	draw.text(position, chinese, font = font, fill = fillColor)

	img = cv2.cvtColor(np.array(img_PIL),cv2.COLOR_RGB2BGR)
	return img

def hist(img):
	img = cv2.calcHist([img], [0], None, [256], [0, 256])
	plt.subplot(121)
	plt.imshow(img, 'gray')
	plt.xticks([])
	plt.yticks([])
	plt.title("Original")
	plt.subplot(122)
	plt.hist(img.ravel(), 256, [0, 256])
	plt.show()