

#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  exit 1
fi

# wsk package update demo

IPV4=$1
UPDATE=$2
PREWARM=$3
RUN=$4

IMAGE1="onanad/action-python-v3.9:profanity"
IMAGE2="onanad/action-python-v3.9:censor"

# docker pull  $IMAGE
if [ "$UPDATE" == "1" ]; then
  ./S2.sh $IPV4 1 0 0 
  docker pull onanad/action-python-v3.9:profanity
  docker pull onanad/action-python-v3.9:censor
  wsk action update guest/demo/profanity  --docker $IMAGE1 profanity/__main__.py --web true
  wsk action update censor --docker $IMAGE2  censor/__main__.py 
  wsk action update coord coord/__main__.py
  wsk action update S3 --sequence coord,censor  
fi

if [ "$PREWARM" == "1" ]; then
  wsk action invoke S3 -r \
    --param ipv4 $IPV4 \
    --param text "1Ko.txt" \
    --param schema "S3"
fi

if [ "$RUN" == "1" ]; then

  mkdir -p "result/energy/S3/" 

  TEXTES=("1Ko.txt" "5Ko.txt" "12Ko.txt" )

  for TEXT in "${TEXTES[@]}"; do

    echo -e "$TEXT" 
    for (( i = 1; i <= 2; i++ )); do
      # Launch cpu-energy-meter in background and save her PID
      cpu-energy-meter -r >> "result/energy/S3/$TEXT" &
      METER_PID=$!

      wsk action invoke S3 -r \
        --param ipv4 "$IPV4" \
        --param schema "S3" \
        --param text "$TEXT" >> "result/result.txt"
      kill -SIGINT $METER_PID

      echo -e "$i"
      
      sleep 6
    
    done

  done
    
fi