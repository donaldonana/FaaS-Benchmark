#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <ipv4> <image> <run>"
  echo "ipv4 : ipv4 for swift connection"
  echo "run  :  run"
  echo "update :  update"
  echo "image  :  image"
  exit 1
fi

IPV4=$1
RUN=$2
UPDATE=$3
VIDEO=$4


if [ "$UPDATE" == "1" ]; then
  docker pull onanad/action-python-v3.9:thumb
  wsk action update thumb --docker onanad/action-python-v3.9:thumb __main__.py  
fi

# Prewarm the container
wsk action invoke thumb --result \
  --param ipv4 "$IPV4" \
  --param file 1Mb.avi \
  --param bib "moviepy"
 
# Run the experiment
if [ "$RUN" == "1" ]; then

  LIBRARY=("moviepy" "ffmpeg" "imageio" "opencv")
  mkdir -p "result/energy/$VIDEO"

  for LIB in "${LIBRARY[@]}"; do
    echo -e "$LIB"  
    ENERGY_FILE="result/energy/$VIDEO/$LIB$VIDEO.txt"  
      
    for (( i = 1; i <= 10; i++ )); do
      # Launch cpu-energy-meter in background and save her PID
      cpu-energy-meter -r >> $ENERGY_FILE &
      METER_PID=$!
      wsk action invoke proc -r \
        --param bib  "$LIB" \
        --param ipv4 "$IPV4" \
        --param file "$VIDEO" >> result/result.txt

      kill -SIGINT $METER_PID
      echo -e "$i"
      
      sleep 2
    done
      
  done

fi

