import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt
from imutils.video import FPS
import time

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')
print("[INFO] model loaded...")


CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
	
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def object_detection(image):
	(h, w) = image.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
	# pass the blob through the network and obtain the detections and
	# predictions
	
	print("[INFO] computing object detections...")
	net.setInput(blob)
	detections = net.forward()
	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]
		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > .60:
			# extract the index of the class label from the `detections`,
			# then compute the (x, y)-coordinates of the bounding box for
			# the object
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			# display the prediction
			label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
			print("[INFO] {}".format(label))
			cv2.rectangle(image, (startX, startY), (endX, endY),
						  COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(image, label, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
	return image


cap = cv2.VideoCapture('/home/ashish/Desktop/skylark_work/Skyfall - Opening Scene_ Motorbike Chase (1080p).mp4')
fps = FPS().start()
while(cap.isOpened()):
	ret, frame = cap.read()

	image=object_detection(frame)
	cv2.imshow('image',image)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	fps.update()
	fps.stop()
	font = cv2.FONT_HERSHEY_SIMPLEX
	# cv2.putText(image,"FPS: {:.2f}".format(fps.fps()),(20,50), font, 1,(0,255,0),2,cv2.LINE_AA)

	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


cap.release()
cv2.destroyAllWindows()