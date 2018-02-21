from PIL import Image
import os

# TODO - Right now it assumes that files in the directory are image file
def resize_all(path_to_directory, new_width = 540):
	""" Resize all the images in the directory

	Args:
		path_to_directory: path of the directory of which images have to be resized
		new_width: width to which image has to be resized

	"""

	# check if directory exists
	if(not os.path.isdir(path_to_directory)):
		print("Given directory doesn't exists")
		return

	successful_resize = 0
	errors = 0

	for filename in os.listdir(path_to_directory):
		try:
			file_path = os.path.join(path_to_directory, filename)
			image = Image.open(file_path)
			ratio = (new_width/float(image.size[0]))
			new_height = int(image.size[1] * float(ratio))
			image = image.resize((new_width, new_height), Image.ANTIALIAS)
			image.save(file_path, 'JPEG')
			successful_resize = successful_resize + 1
		except Exception as e:
			print("Error resizing")
			print(e)
			errors = errors + 1
	
	if(successful_resize > 0):
		print("Resized {} images".format(successful_resize))	

	if(errors > 0):
		print("with {} errors".format(errors))	