import os
import io
import glob
import hashlib
import pandas as pd
import xml.etree.ElementTree as ET
import tensorflow as tf
import random

from PIL import Image
from object_detection.utils import dataset_util

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


'''
this script automatically divides dataset into training and evaluation (10% for evaluation)
this scripts also shuffles the dataset before converting it into tfrecords
if u have different structure of dataset (rather than pascal VOC ) u need to change
the paths and names input directories(images and annotation) and output tfrecords names.
(note: this script can be enhanced to use flags instead of changing parameters on code).
default expected directories tree:
dataset- 
   -raw_images
   -annotations
    create_tfrecord.py   
to run this script:
$ python dataset_to_tfrecord.py 
'''
def create_example(xml_file):
        #process the xml file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        image_name = root.find('filename').text
        print(image_name)
        file_name = image_name.encode('utf8')
        size=root.find('size')
        width = int(size[0].text)
        height = int(size[1].text)
        xmin = []
        ymin = []
        xmax = []
        ymax = []
        classes = []
        classes_text = []
        truncated = []
        poses = []
        difficult_obj = []
        for member in root.findall('object'):
           #classes_text.append('Avocado'.encode('utf8'))
	   classes_text.append(member[0].text.encode('utf8'))
	   print(member[0].text)
           xmin.append(float(member[4][0].text) / width)
           ymin.append(float(member[4][1].text) / height)
           xmax.append(float(member[4][2].text) / width)
           ymax.append(float(member[4][3].text) / height)
           difficult_obj.append(0)
           #if you have more than one classes in dataset you can change the next line
           #to read the class from the xml file and change the class label into its 
           #corresponding integer number, u can use next function structure
           
           def class_text_to_int(row_label):
              if row_label == 'calbee':
                  return 1
              if row_label == 'g_pretz':
                return 2


           classes.append(class_text_to_int(member[0].text))   # i wrote 1 because i have only one class(person)
           truncated.append(0)
	   print(class_text_to_int(member[0].text))
           poses.append('Unspecified'.encode('utf8'))

        #read corresponding image
        full_path = os.path.join('data/raw_images', '{}'.format(image_name))  #provide the path of images directory
        with tf.gfile.GFile(full_path, 'rb') as fid:
            encoded_jpg = fid.read()
        encoded_jpg_io = io.BytesIO(encoded_jpg)
        image = Image.open(encoded_jpg_io)
        if image.format != 'JPEG':
           raise ValueError('Image format not JPEG')
        key = hashlib.sha256(encoded_jpg).hexdigest()
		
        #create TFRecord Example
        example = tf.train.Example(features=tf.train.Features(feature={
            'image/height': dataset_util.int64_feature(height),
            'image/width': dataset_util.int64_feature(width),
            'image/filename': dataset_util.bytes_feature(file_name),
            'image/source_id': dataset_util.bytes_feature(file_name),
            'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
            'image/encoded': dataset_util.bytes_feature(encoded_jpg),
            'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
            'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
            'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
            'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
            'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
            'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes),
            'image/object/difficult': dataset_util.int64_list_feature(difficult_obj),
            'image/object/truncated': dataset_util.int64_list_feature(truncated),
            'image/object/view': dataset_util.bytes_list_feature(poses),
        }))	
        return example	
		
def main(_):
    writer_train = tf.python_io.TFRecordWriter('data/train.record')     
    writer_test = tf.python_io.TFRecordWriter('data/val.record')
    #provide the path to annotation xml files directory
    filename_list=tf.train.match_filenames_once("data/annotations/*.xml")
    print(filename_list)
    init = (tf.global_variables_initializer(), tf.local_variables_initializer())
    sess=tf.Session()
    sess.run(init)
    list=sess.run(filename_list)
    random.shuffle(list)   #shuffle files list
    i=1 
    tst=0   #to count number of images for evaluation 
    trn=0   #to count number of images for training
    for xml_file in list:
      example = create_example(xml_file)
      if (i%10)==0:  #each 10th file (xml and image) write it for evaluation
         writer_test.write(example.SerializeToString())
         tst=tst+1
      else:          #the rest for training
         writer_train.write(example.SerializeToString())
         trn=trn+1
      i=i+1
      print(xml_file)
    writer_test.close()
    writer_train.close()
    print('Successfully converted dataset to TFRecord.')
    print('training dataset: # ')
    print(trn)
    print('test dataset: # ')
    print(tst)	
	
if __name__ == '__main__':
    tf.app.run()
