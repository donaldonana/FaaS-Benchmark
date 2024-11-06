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
  docker pull onanad/action-python-v3.9:imgrec
  wsk action update imgrec -m 1024 --docker onanad/action-python-v3.9:imgrec __main__.py  
fi

# Prewarm the container
wsk action invoke imgrec --result  --param ipv4 "$IPV4"  --param image 1Mb.JPEG --param resnet resnet152

# Run the experiment
if [ "$RUN" == "1" ]; then

  MODEL=("resnet18" "resnet34" "resnet50" "resnet152")
  mkdir -p "result/energy/$IMAGE" 
  
  for MOD in "${MODEL[@]}"; do
    echo -e "$MOD"  
    ENERGY_FILE="result/energy/$IMAGE/$MOD$IMAGE.txt"  

    for (( i = 1; i <= 10; i++ )); do
      # Launch cpu-energy-meter in background and save her PID
      cpu-energy-meter -r >> "$ENERGY_FILE" &
      METER_PID=$!
      wsk action invoke imgrec -r \
        --param resnet "$MOD" \
        --param ipv4   "$IPV4" \
        --param image  "$IMAGE" >>  result/result.txt

      kill -SIGINT $METER_PID

      echo -e "$i"
      
      sleep 2
    done

  done

fi 

