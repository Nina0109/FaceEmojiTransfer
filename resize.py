import cv2
import time 
import numpy as np

if __name__ == '__main__':
	imgname = "test6.jpg"
	img = cv2.imread(imgname)
	px = 250
	py = 250

	paddedped_img = np.pad(img,((py,py),(px,px),(0,0)), 'constant',constant_values=0)
	cv2.imwrite("padded.jpg",paddedped_img)