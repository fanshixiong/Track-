import numpy as np
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.pyplot as plt
import math

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


def show_precision(positions, ground_truth):
	max_threshold = 50
	#print(type(positions))
	#print(type(ground_truth))
	if (positions.shape != ground_truth.shape):
		print("Could not plot precisions, because  the number of ground_")
		print("truth frames does not match the number of tracked frames.")
		return
	length = positions.shape[0]

	target = np.zeros([length, 2])
	for i in range(length + 1):
		target[i-1, 0] = ground_truth[i - 1, 0] + 0.5*ground_truth[i-1, 2]
		target[i - 1, 0] = int(target[i-1, 0])
		target[i-1, 1] = ground_truth[i - 1, 1] + 0.5*ground_truth[i-1, 3]
		target[i - 1, 1] = int(target[i - 1, 1])

	pos = np.zeros([length, 2])
	for i in range(length + 1):
		pos[i-1, 0] = positions[i - 1, 0] + 0.5*positions[i-1, 2]
		pos[i-1, 1] = positions[i - 1, 1] + 0.5*positions[i-1, 3]
	distances = np.zeros([length, 1])
	for i in range(distances.shape[0]+1):
		#print("pos",pos[i - 1])
		#print("target", target[i - 1])
		distances[i-1] = math.sqrt(np.power((pos[i-1, 0] - target[i-1, 0]), 2)+ np.power((pos[i-1, 1] - target[i-1, 1]), 2))


	precisions = np.zeros([max_threshold+1, 1])
	p = 1
	while(p <= max_threshold):
		#print(p)
		#print(np.sum(distances < p))
		precisions[p] = np.sum(distances < p)/np.size(distances)
		p += 1
	x = np.arange(max_threshold + 1)
	plt.plot(x, precisions)
	plt.show()
