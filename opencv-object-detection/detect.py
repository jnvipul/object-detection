import cv2
from matplotlib import pyplot as plt
from math import cos, sin
import numpy as np
from __future__ import division

def find_object(image):

	# Color scheme
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# Scale
	max_dimension = max(image.shape)
	scale = 700/max_dimension
	image = cv2.resize(image, None, fx=scale, fy=scale)

	# clean image
	image_blur = cv2.GaussianBlur(image, (7, 7), 0)
	image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR.RGB2HSV)
	
