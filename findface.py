import cv2
import time 
import numpy as np

def crop_face_new(img_name,out_name):
		img = cv2.imread(img_name)
		height,width = img.shape[0],img.shape[1]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		haar_face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
		faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
		(x,y,w,h) = faces[0]

		center_x = int(x + w/2)
		center_y = int(y + h/2)

		x_min = max(0,center_x-4*w)  #3/4 #4/5
		x_max = min(width,center_x+4*w)
		y_min = max(0,center_y-4*h)
		y_max = min(height,center_y+4*h) 

		print("width, height: ",width,height)
		print("center: ",center_x,center_y)
		print("whole face: ",x_min,x_max,y_min,y_max)

		whole_face = img[int(y_min):int(y_max),int(x_min):int(x_max),:]

		if y_max-y_min <512 and x_max-x_min<512: 
			print("Find face smaller than 512.")

			x_min = max(0,center_x-256)
			x_max = min(width,center_x+256)
			y_min = max(0,center_y-256)
			y_max = min(height,center_y+256) 
			whole_face = img[int(y_min):int(y_max),int(x_min):int(x_max),:]

			p1 = max(center_x-x_min,x_max-center_x,center_y-y_min,y_max-center_y)
			px1 = p1-(center_x-x_min)
			px2 = p1-(x_max-center_x)
			py1 = p1-(center_y-y_min)
			py2 = p1-(y_max-center_y)
			whole_face = np.pad(whole_face,((int(py1),int(py2)),(int(px1),int(px2)),(0,0)),'constant',constant_values=255)

			if(whole_face.shape[0] < 512):
				padded_img = cv2.resize(whole_face,(512,512))
			else:
				padded_img = whole_face

			# px1 = 256-(center_x-x_min)
			# px2 = 256-(x_max-center_x)
			# py1 = 256-(center_y-y_min)
			# py2 = 256-(y_max-center_y)
			# print("padding: ",px1,px2,py1,py2)

			# padded_img = np.pad(whole_face,((int(py1),int(py2)),(int(px1),int(px2)),(0,0)),'constant',constant_values=255)

		else:
			print("Find face bigger than 512.")
			print(whole_face.shape)
			p1 = max(center_x-x_min,x_max-center_x,center_y-y_min,y_max-center_y)
			px1 = p1-(center_x-x_min)
			px2 = p1-(x_max-center_x)
			py1 = p1-(center_y-y_min)
			py2 = p1-(y_max-center_y)
			print("p1: ",p1)
			print("padding: ",px1,px2,py1,py2)

			whole_face = np.pad(whole_face,((int(py1),int(py2)),(int(px1),int(px2)),(0,0)),'constant',constant_values=255)
			print(whole_face.shape)
			# whole_face = cv2.resize(whole_face,(512,512))

			# final version
			#---------------------------------------------------------
			padded_img = cv2.resize(whole_face,(1000,1000))
			#---------------------------------------------------------
			# padded_img = whole_face

			# padded_img = np.pad(whole_face,((256,256),(256,256),(0,0)),'constant',constant_values=255)


		cv2.imwrite(out_name,padded_img)
		print("Processed img saved to:",out_name)


def crop_face(img_name,out_name):
		img = cv2.imread(img_name)
		height,width = img.shape[0],img.shape[1]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		haar_face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
		faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
		(x,y,w,h) = faces[0]

		center_x = int(x + w/2)
		center_y = int(y + h/2)

		w_hat = min(w/2 + w,center_x,width-center_x)  #w/3
		h_hat = min(h/2 + h,center_y,height-center_y) #h/3

		if min(w,h) < 1000:  # 512
			print("Face is small than 512")
			padding = 600
			padding_x = min(padding,center_x,width-center_x)
			padding_y = min(padding,center_y,height-center_y)
			croped_img = img[center_y-padding_y:center_y+padding_y,center_x-padding_x:center_x+padding_x,:]
			y_min = center_y-padding_y
			y_max = center_y+padding_y
			x_min = center_x-padding_x
			x_max = center_x+padding_x

			p1 = max(center_x-x_min,x_max-center_x,center_y-y_min,y_max-center_y)
			px1 = p1-(center_x-x_min)
			px2 = p1-(x_max-center_x)
			py1 = p1-(center_y-y_min)
			py2 = p1-(y_max-center_y)

			croped_img = np.pad(croped_img,((int(py1),int(py2)),(int(px1),int(px2)),(0,0)),'constant',constant_values=255)
			if(croped_img.shape[0]<600):
				croped_img = cv2.resize(croped_img,(700,700))

		else:
			print("Face is bigger than 512")
			padding = int(max(w*3.5,h*3.5))
			# padding = int(max(w*2/3,h*2/3))
			padding_x = min(padding,width-x-w,x)
			padding_y = min(padding,height-y-h,y)
			# y_min = max(0,y-padding_y)
			# y_max = min(y+h+padding_y,height)
			# x_min = max(0,x-padding_x)
			# x_max = min(x+w+padding_x,width)

			y_min = y-padding_y
			y_max = y+h+padding_y
			x_min = x-padding_x
			x_max = x+w+padding_x

			print(x_min,x_max,y_min,y_max)
			croped_img = img[y_min:y_max,x_min:x_max,:]



		deta_x = int((x_max - x_min)/2)
		deta_y = int((y_max - y_min)/2)
			
		# croped_img = img[y:y+h,x:x+w,:]
		# scale = 2*padding+w
		if deta_x>deta_y:
			print('padded: deta_x>deta_y')
			croped_img = np.pad(croped_img,((deta_x-deta_y,deta_x-deta_y),(0,0),(0,0)), 'constant',constant_values=255)
		else:
			print('padded: deta_x<=deta_y')
			croped_img = np.pad(croped_img,((0,0),(deta_y-deta_x,deta_y-deta_x),(0,0)), 'constant',constant_values=255)

			# 'constant',constant_values=255)
		croped_img = cv2.resize(croped_img,(1000,1000))  #512

		cv2.imwrite(out_name,croped_img)
		print("Processed img saved to:",out_name)


def crop_face_backup(img_name,out_name):
		img = cv2.imread(img_name)
		height,width = img.shape[0],img.shape[1]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		haar_face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
		faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
		(x,y,w,h) = faces[0]

		center_x = int(x + w/2)
		center_y = int(y + h/2)

		w_hat = min(w/2 + w/3,center_x,width-center_x)
		h_hat = min(h/2 + h/3,center_y,height-center_y)

		if min(w,h) < 512:
			print("Face is small than 512")
			padding = 400
			padding_x = min(padding,center_x,width-center_x)
			padding_y = min(padding,center_y,height-center_y)
			croped_img = img[center_y-padding_y:center_y+padding_y,center_x-padding_x:center_x+padding_x,:]

		else:
			print("Face is bigger than 512")
			padding = int(max(w*1.5/3,h*1.5/3))
			padding_x = min(padding,width-x-w,x)
			padding_y = min(padding,height-y-h,y)
			# y_min = max(0,y-padding_y)
			# y_max = min(y+h+padding_y,height)
			# x_min = max(0,x-padding_x)
			# x_max = min(x+w+padding_x,width)

			y_min = y-padding_y
			y_max = y+h+padding_y
			x_min = x-padding_x
			x_max = x+w+padding_x

			print(x_min,x_max,y_min,y_max)
			croped_img = img[y_min:y_max,x_min:x_max,:]



		deta_x = int((x_max - x_min)/2)
		deta_y = int((y_max - y_min)/2)
			
		# croped_img = img[y:y+h,x:x+w,:]
		# scale = 2*padding+w
		if deta_x>deta_y:
			print('padded: deta_x>deta_y')
			croped_img = np.pad(croped_img,((deta_x-deta_y,deta_x-deta_y),(0,0),(0,0)), 'constant',constant_values=0)
		else:
			print('padded: deta_x<=deta_y')
			croped_img = np.pad(croped_img,((0,0),(deta_y-deta_x,deta_y-deta_x),(0,0)), 'constant',constant_values=0)

			# 'constant',constant_values=255)
		# croped_img = cv2.resize(croped_img,(520,520))

		cv2.imwrite(out_name,croped_img)
		print("Processed img saved to:",out_name)

if __name__ == '__main__':
	# img = cv2.imread('sjh.png')
	# height,width = img.shape[0],img.shape[1]
	# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# haar_face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
	# faces = haar_face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
	# (x,y,w,h) = faces[0]


	# center_x = int(x + w/2)
	# center_y = int(y + h/2)

	# x_min = max(0,center_x-300)
	# y_min = max(0,center_y-300)

	# x_max = min(center_x+300,width)
	# y_max = min(center_y+300,height)

	# print(y_min,y_max,x_min,x_max)
	# croped_img = img[y_min:y_max,x_min:x_max,:]
	# cv2.imwrite('croped.jpg',croped_img)

	crop_face('test6.jpg','padded.jpg')


