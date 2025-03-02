#!/bin/bash

IMAGE="1Mb.JPEG"
IPV4="172.20.20.77"
LIBRARY=("pillow" "wand" "pygame" "opencv")

mkdir -p "result/energy/energy/$IMAGE" 

for LIB in "${LIBRARY[@]}"; do

  echo -e "$LIB"
  ENERGY_FILE="result/energy//energy/$IMAGE/$LIB$IMAGE.txt"  

  for (( i = 1; i <= 10; i++ )); do
 
    # Launch cpu-energy-meter in background and save its PID
    cpu-energy-meter -r >> "$ENERGY_FILE" &
    METER_PID=$!
      
    wsk action invoke thumb -r \
      --param bib  "$LIB" \
      --param ipv4 "$IPV4" \
      --param file "$IMAGE" >> result/energy/result.txt

    kill -SIGINT "$METER_PID"

    echo -e "$i"

    sleep 2
      
  done

done

 

