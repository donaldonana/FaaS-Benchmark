#!/bin/bash

IPV4="10.245.158.103"
IMAGES=("500b.JPEG" "100Kb.JPEG" "1Mb.JPEG" "15Mb.JPEG" "256Kb.JPEG")
LIBRARY=("pillow" "wand" "pygame" "opencv")


for IMAGE in "${IMAGES[@]}"; do
  wskdeploy > /dev/null
  wsk  action invoke thumb -r --param ipv4 "$IPV4" > /dev/null   # Manually prewarm the container
  mkdir -p "result/energy/$IMAGE" 
  echo -e "$IMAGE"


  for LIB in "${LIBRARY[@]}"; do
    echo -e "$LIB"
    ENERGY_FILE="result/energy/$IMAGE/$LIB$IMAGE.txt"  

    for (( i = 1; i <= 50; i++ )); do  
      cpu-energy-meter -r >> "$ENERGY_FILE" &     # Launch cpu-energy-meter in background and save its PID
      METER_PID=$!
      
      wsk action invoke thumb -r \
        --param bib  "$LIB" \
        --param ipv4 "$IPV4" \
        --param file "$IMAGE" >> result/result.txt #test

      kill -SIGINT "$METER_PID"
      echo -e "$i"
      sleep 2

    done

    sleep 2
    
  done

done

 

