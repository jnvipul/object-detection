import numpy as np
import cv2
import sys
import os


if len(sys.argv) < 2:
	sys.exit("Object name is missing, run the script with a string as a param")

object_name = sys.argv[1]

# create directory
if not os.path.exists(object_name):
    os.makedirs(object_name)

print "Name of the Object : ", object_name

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter(object_name + "/" + object_name + ".mp4", fourcc, 2, size)

count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

        # write the frame 
        out.write(frame)
        cv2.imwrite(object_name + "/" + object_name + "_%d.jpg" % count, frame)
        count += 1

		# write the video
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()