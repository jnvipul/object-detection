import boto3
import sys
import os

bucket_name = "honestbee-staging-product-object-recognition"

def upload_directory(src_dir, bucket_name, dst_dir):
	print "Starting upload"
	if not os.path.isdir(src_dir):
		raise ValueError('src_dir %r not found.' % src_dir)

	all_files = []

	for root, dirs, files in os.walk(src_dir):
		all_files += [os.path.join(root, f) for f in files]

	s3_resource = boto3.resource('s3')

	for filename in all_files:
		print ("Starting upload for %s" %filename)
		s3_resource.Object(bucket_name, os.path.join(dst_dir, os.path.relpath(filename, src_dir)))\
		.put(Body=open(filename, 'rb'))


if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit("Directory name is missing, run the script with a string as a param")

	upload_directory(sys.argv[1], bucket_name, sys.argv[1])
