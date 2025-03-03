#!/bin/bash

IPV4="172.20.20.77"
MODEL=("resnet18" "resnet34" "resnet50" "resnet152")
IMAGES=("100Kb.JPEG" "500b.JPEG" "1Mb.JPEG" "15Mb.JPEG" "256Kb.JPEG")

for IMAGE in "${IMAGES[@]}"; do
  echo -e "$IMAGE"
  mkdir -p "result/energy/$IMAGE" 

  for MOD in "${MODEL[@]}"; do
    echo -e "$MOD"
    ENERGY_FILE="result/energy/$IMAGE/$MOD$IMAGE.txt"  

    for (( i = 1; i <= 100; i++ )); do
      # Launch cpu-energy-meter in background and save its PID
      cpu-energy-meter -r >> "$ENERGY_FILE" &
      METER_PID=$!

      wsk action invoke imgrec -r \
        --param image  "$IMAGE" \
        --param ipv4 "$IPV4" \
        --param resnet "$MOD" >> result/result.txt

      kill -SIGINT "$METER_PID"
      echo -e "$i"
      sleep 4

    done

    sleep 4
    
  done

done
 
