#!/bin/bash

if [ "$#" -ne 2 ]; then

  echo "Usage: $0 <ipv4> <image>"
  echo "ipv4 : ipv4 for swift connection"
  echo "image : image "
  exit 1
fi

IPV4=$1

IMAGE=$2

# Library List
LIBRARY=("pillow" "wand" "pygame" "opencv")

RESULT_FILE="result/result.txt"

ENERGY_DIR="result/energy"

mkdir -p "$ENERGY_DIR/$IMAGE" 
 
 
for LIB in "${LIBRARY[@]}"; do

  echo -e "$LIB"  

  ENERGY_FILE="$ENERGY_DIR/$IMAGE/$LIB$IMAGE.txt"  
    
  for (( i = 1; i <= 10; i++ )); do
    	 
    # Launch cpu-energy-meter in background and save her PID
    cpu-energy-meter -r >> $ENERGY_FILE &
    METER_PID=$!

    wsk action invoke thumb -r \
      --param bib "$LIB" \
      --param ipv4 "$IPV4" \
      --param file "$IMAGE" >> $RESULT_FILE

    kill -SIGINT $METER_PID

    echo -e "$i"
		
		sleep 2
	
  done
    
done
