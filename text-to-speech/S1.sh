
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  exit 1
fi

IPV4=$1
TEXTES=("1Ko.txt" "5Ko.txt" "12Ko.txt")
IMAGE="onanad/action-python-v3.9:text2speech"

# docker pull  $IMAGE

wsk package update demo

wsk action update guest/demo/text2speech \
  --docker $IMAGE \
  speech/__main__.py \
  --web true

wsk action invoke demo/text2speech -r \
  --param ipv4 $IPV4 \
  --param schema "S1" \
  --param text "12Ko.txt"

mkdir -p "result/energy/S1/" 

for TEXT in "${TEXTES[@]}"; do
  echo -e "$TEXT" 
  for (( i = 1; i <= 2; i++ )); do
    # Launch cpu-energy-meter in background and save her PID
    cpu-energy-meter -r >> "result/energy/S1/$TEXT" &
    METER_PID=$!

    wsk action invoke demo/text2speech -r \
      --param ipv4 "$IPV4" \
      --param schema "S1" \
      --param text "$TEXT" >> "result/result.txt"
    kill -SIGINT $METER_PID

    echo -e "$i"
    sleep 6
    
  done

done
    