
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
  wsk action invoke demo/text2speech -r --param ipv4 $IPV4 --param schema "S1"
}

run() {
  for (( i = 1; i <= 30; i++ )); 
  do
    cpu-energy-meter -r >> "result/energy/S1/energy.txt" &
    METER_PID=$!

    wsk action invoke demo/text2speech -r \
      --param ipv4 "$IPV4" \
      --param schema "S1" >>  "result/result.txt"
    kill -SIGINT $METER_PID

    echo -e "$i"

    sleep 4
	
  done
}

echo -e "---->Pull Docker image begin" & pull
echo -e "---->Prewarm Docker image begin" & prewarm
mkdir -p "result/energy/S1/" 
echo -e "---->Experiment begin" & run