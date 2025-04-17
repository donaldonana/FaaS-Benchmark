#!/bin/bash

IPV4="172.20.20.78"
VIDEOS=("1Mb.avi" "6Mb.avi" "36Kb.avi" "540Kb.avi")
LIBRARY=("moviepy" "ffmpeg" "imageio" "opencv")
 
for VIDEO in "${VIDEOS[@]}"; do
  echo  -e "$VIDEO"
  mkdir -p "result/energy/$VIDEO" 

  for LIB in "${LIBRARY[@]}"; do
    echo -e "$LIB"
    ENERGY_FILE="result/energy/$VIDEO/$LIB$VIDEO.txt"  

    for (( i = 1; i <= 100; i++ )); do

      cpu-energy-meter -r >> "$ENERGY_FILE" &
      METER_PID=$!

      wsk action invoke proc -r \
          --param bib  "$LIB" \
          --param ipv4 "$IPV4" \
          --param file "$VIDEO" >> result/result.txt

      kill -SIGINT "$METER_PID"
      echo -e "$i"
      sleep 2
        
    done

    sleep 2

  done

done
