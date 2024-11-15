
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
IMAGE="onanad/action-python-v3.9:conversion"

# docker pull  $IMAGE
if [ "$UPDATE" == "1" ]; then
  ./S1.sh $IPV4 1 0 0 
  docker pull onanad/action-python-v3.9:conversion
  wsk action update guest/demo/conversion  --docker $IMAGE  conversion/__main__.py  --web true
  wsk action update guest/demo/S2  --sequence demo/text2speech,demo/conversion  --web true
fi

if [ "$PREWARM" == "1" ]; then
  wsk action invoke demo/S2 -r \
    --param ipv4 $IPV4 \
    --param text "1Ko.txt" \
    --param schema "S2"
fi

if [ "$RUN" == "1" ]; then

  mkdir -p "result/energy/S2/" 

  TEXTES=("1Ko.txt" "5Ko.txt" "12Ko.txt")

  for TEXT in "${TEXTES[@]}"; do

    echo -e "$TEXT" 
    for (( i = 1; i <= 2; i++ )); do
      # Launch cpu-energy-meter in background and save her PID
      cpu-energy-meter -r >> "result/energy/S2/$TEXT" &
      METER_PID=$!

      wsk action invoke demo/S2 -r \
        --param ipv4 "$IPV4" \
        --param schema "S2" \
        --param text "$TEXT" >> "result/result.txt" 
      kill -SIGINT $METER_PID

      # perf stat -o result/perfEnergyS1.txt --append -e power/energy-pkg/ -e power/energy-cores/ wsk action invoke demo/text2speech -r --param ipv4 "$IPV4"  --param schema "S1" --param text "$TEXT" >> "result/perf.txt"

      echo -e "$i"
      
      sleep 6
      
    done
    
  done
    
fi
