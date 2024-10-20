#!/bin/bash

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <ipv4> <image> <run>"
  echo "ipv4 : ipv4 for swift connection"
  echo "image : image "
  echo "run :  run "
  exit 1
fi

IPV4=$1
IMAGE=$2
RUN=$3
BUILD="pull"

if [ "$BUILD" != "push" ] && [ "$BUILD" != "pull" ]; then
  echo "Invalid build argument. Expected 'push' or 'pull'."
  exit 1   
fi

if [ "$BUILD" == "push" ]; then
  echo "comming son"
else
  docker pull onanad/action-python-v3.9:thumb
  wsk action update thumb --docker onanad/action-python-v3.9:thumb __main__.py  
fi

# Prewarm the container
wsk action invoke thumb --result  --param ipv4 "$IPV4"  --param file 1Mb.JPEG --param bib "pillow"

# Run the experiment
if [ "$RUN" == "1" ]; then
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

fi

