#!/bin/bash

if [ "$#" -ne 2 ]; then

  echo "Usage: $0 <ipv4> <image>"
  echo "ipv4 : ipv4 for swift connection"
  echo "image : image "
  exit 1
fi

IPV4=$1

IMAGE=$2
 
build="pull"

if [ "$build" != "push" ] && [ "$build" != "pull" ]; then

    echo "Invalid build argument. Expected 'push' or 'pull'."
    exit 1   
fi

if [ "$build" == "push" ]; then
    echo "comming son"
else
    docker pull onanad/action-python-v3.9:imgrec
fi

wsk action update imgrec --timeout 300000 --memory 1024 --docker onanad/action-python-v3.9:imgrec __main__.py --web true

wsk action invoke imgrec --result  --param ipv4 "$IPV4"  --param image 1Mb.JPEG --param resnet resnet152

echo -e "---start"

# Library List
MODEL=("resnet18" "resnet34" "resnet50" "resnet152")

RESULT_FILE="result/result.txt"

ENERGY_DIR="result/energy"

mkdir -p "$ENERGY_DIR/$IMAGE" 
 
for MOD in "${MODEL[@]}"; do

  echo -e "$MOD"  
  ENERGY_FILE="$ENERGY_DIR/$IMAGE/$MOD$IMAGE.txt"  
    
  for (( i = 1; i <= 10; i++ )); do
    # Launch cpu-energy-meter in background and save her PID
    cpu-energy-meter -r >> $ENERGY_FILE &
    METER_PID=$!

    wsk action invoke imgrec -r \
      --param resnet "$MOD" \
      --param ipv4 "$IPV4" \
      --param image "$IMAGE" >> $RESULT_FILE

    kill -SIGINT $METER_PID

    echo -e "$i"
		
	sleep 2
	
  done
    
done
