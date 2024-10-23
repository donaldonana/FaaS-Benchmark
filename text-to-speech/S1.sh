
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  exit 1
fi

IPV4=$1

pull() {
  IMAGE="onanad/action-python-v3.9:text2speech"
  docker pull  $IMAGE
  wsk action update guest/demo/text2speech --docker $IMAGE speech/__main__.py --web true
}

prewarm() {
  wsk action invoke demo/text2speech -r --param ipv4 $IPV4 --param schema "S1" --param text "1Ko.txt"
}

echo -e "--->Pull Docker image begin"
pull
echo -e "--->Prewarm Docker image begin"
prewarm

echo -e "--->Experiment begin"
mkdir -p "result/energy/S1/" 

mkdir -p "result/energy/S1/" 

TEXTES=("1Ko.txt" "5Ko.txt" "12Ko.txt")

for TEXT in "${TEXTES[@]}"; do

  echo -e "$TEXT" 
  for (( i = 1; i <= 8; i++ )); do
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
    