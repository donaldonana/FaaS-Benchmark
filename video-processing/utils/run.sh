#!/bin/bash

if [ "$#" -ne 2 ]; then

  echo "Usage: $0 <ipv4> <video>"
  echo "ipv4 : ipv4 for swift connection"
  echo "Video : Video "
  exit 1
fi

IPV4=$1

VIDEO=$2

# Library List
LIBRARY=("moviepy" "ffmpeg" "imageio" "opencv")

RESULT_FILE="result/result.txt"

ENERGY_DIR="result/energy"

mkdir -p "$ENERGY_DIR/$VIDEO" 
 
 
# Iterate over each library in the array
for LIB in "${LIBRARY[@]}"; do

  echo -e "$LIB" 

  ENERGY_FILE="$ENERGY_DIR/$VIDEO/$LIB$VIDEO.txt"  
    
  for (( i = 1; i <= 10; i++ )); do
    	 
    # Launch cpu-energy-meter in background and save her PID
		cpu-energy-meter -r >> $ENERGY_FILE &
		METER_PID=$!
		
		wsk action invoke proc -r \
      --param bib "$LIB" \
      --param ipv4 "$IPV4" \
      --param file "$VIDEO" >> $RESULT_FILE

		kill -SIGINT $METER_PID
	
	  echo -e "$i"

	  sleep 2
	
  done
    
done
