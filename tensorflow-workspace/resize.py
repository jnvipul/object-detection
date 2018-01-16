from PIL import Image
import tensorflow as tf
import os
import numpy as np

image_folder_cur = 'cola_1x_a'
image_folder_des = 'cola_1x_a_small'
images = [img for img in os.listdir(image_folder_cur) if img.endswith(".jpg")]

def load_image_into_numpy_array(image):
	(im_width, im_height) = image.size
	return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
# np_images = 
for image in images:
	im1 = Image.open(os.path.join(image_folder_cur,image))
	basewidth = 300
	wpercent = (basewidth / float(im1.size[0]))
	hsize = int((float(im1.size[1]) * float(wpercent)))
	im1 = im1.resize((basewidth, hsize), Image.ANTIALIAS)
	np_image = load_image_into_numpy_array(im1)
	print(np_image.shape)
	result = tf.image.resize_image_with_crop_or_pad(np_image,300,300)
	print(type(result))
	print(tf.shape(result))
	# result.save(os.path.join(image_folder_des,image))
	# tf_image = tf.constant(im1)
	# tf_mage = tf.transpose(tf_image, perm=[0,2,1])
	# tf_image = tf.expand_dims(tf_images, 2)
	# resized = tf.image.resize_image_with_crop_or_pad(tf_images,height,width)
	



# for img in tf_images:
# 	im1 = tf.resize_image_with_crop_or_pad(image_np, 300, 300)
# 	im1.save(os.path.join(image_folder_des,image))
