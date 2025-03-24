#!/bin/bash

IPV4="172.20.20.80"

LIBRARY=("pillow" "wand" "pygame" "opencv")
IMAGES=("100Kb.JPEG" "500b.JPEG" "1Mb.JPEG" "15Mb.JPEG" "256Kb.JPEG")

for IMAGE in "${IMAGES[@]}"; do
  echo -e "$IMAGE"
  mkdir -p "result/energy/$IMAGE" 

  for LIB in "${LIBRARY[@]}"; do
    echo -e "$LIB"
    ENERGY_FILE="result/energy/$IMAGE/$LIB$IMAGE.txt"  

    for (( i = 1; i <= 100; i++ )); do  
      cpu-energy-meter -r >> "$ENERGY_FILE" &     # Launch cpu-energy-meter in background and save its PID
      METER_PID=$!
      
      wsk action invoke thumb -r \
        --param bib  "$LIB" \
        --param ipv4 "$IPV4" \
        --param file "$IMAGE" >> result/result.txt

      kill -SIGINT "$METER_PID"
      echo -e "$i"
      sleep 2

    done

    sleep 2
    
  done

done

 

