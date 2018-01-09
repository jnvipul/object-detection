#!/bin/sh

# function cleanup {
# 	echo "Stopping cameras"
# 	pkill -f start.py
# 	pkill -f start2.py
# }



# execute recording script
python start.py $1 &
python start2.py $1

# Kill the first script
pkill -f start.py

# start uploading to s3
python upload.py $1

# while true; do
# 	echo "Press s to stop the recording"
# 	read input
# 	# echo $input
# 	if($input == "s"); then
# 		# cleanup()
# 		break
# 	fi
# done	
