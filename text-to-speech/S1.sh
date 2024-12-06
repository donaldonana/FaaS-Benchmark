
#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  echo "update : update"
  echo "prewarm : prewarm"
  echo "run : run"
  exit 1
fi

IPV4=$1
UPDATE=$2
PREWARM=$3
RUN=$4

TEXTES=("1Ko.txt" "5Ko.txt" "12Ko.txt")
IMAGE="onanad/action-python-v3.9:text2speech"

wsk package update demo

# docker pull  $IMAGE
if [ "$UPDATE" == "1" ]; then
  docker pull $IMAGE
  wsk action update guest/demo/text2speech \
  --docker $IMAGE \
  speech/__main__.py \
  --web true 
fi

if [ "$PREWARM" == "1" ]; then
  wsk action invoke demo/text2speech -r \
    --param ipv4 $IPV4 \
    --param schema "S1" \
    --param text "12Ko.txt"
fi

# Run the experiment
if [ "$RUN" == "1" ]; then

  mkdir -p "result/energy/S1/" 

  for TEXT in "${TEXTES[@]}"; do

    echo "$TEXT" 
    echo -e "$TEXT" >> perfEnergy.txt

    for (( i = 1; i <= 10 ; i++ )); do
    
      # Launch cpu-energy-meter in background and save her PID
      cpu-energy-meter -r >> "result/energy/S1/$TEXT" &
      METER_PID=$!

      wsk action invoke demo/text2speech -r \
        --param ipv4 "$IPV4" \
        --param schema "S1" \
        --param text "$TEXT" >> "result/result.txt"
      kill -SIGINT $METER_PID

      # perf stat -o result/perfEnergyS1.txt --append -e power/energy-pkg/ -e power/energy-cores/ wsk action invoke demo/text2speech -r --param ipv4 "$IPV4"   --param schema "S1" --param text "$TEXT" >> "result/perf.txt"

      echo -e "$i"
      sleep 6
      
    done

  done

fi

