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
IMAGE=$4

if [ "$UPDATE" == "1" ]; then
  docker pull onanad/action-python-v3.9:thumb
  wsk action update thumb --docker onanad/action-python-v3.9:thumb __main__.py  
fi

# Prewarm the container
wsk action invoke thumb --result \  
  --param ipv4 "$IPV4" \
  --param file 1Mb.JPEG \
  --param bib "pillow"

# Run the experiment
if [ "$RUN" == "1" ]; then

  LIBRARY=("pillow" "wand" "pygame" "opencv")
  mkdir -p "result/energy/$IMAGE" 

  for LIB in "${LIBRARY[@]}"; do

    echo -e "$LIB"
    ENERGY_FILE="result/energy/$IMAGE/$LIB$IMAGE.txt"  

    for (( i = 1; i <= 10; i++ )); do

      # Launch cpu-energy-meter in background and save its PID
      cpu-energy-meter -r >> "$ENERGY_FILE" &
      METER_PID=$!
      
      wsk action invoke thumb -r \
        --param bib  "$LIB" \
        --param ipv4 "$IPV4" \
        --param file "$IMAGE" >> result/result.txt

      kill -SIGINT "$METER_PID"

      echo -e "$i"

      sleep 2
      
    done

  done

fi




