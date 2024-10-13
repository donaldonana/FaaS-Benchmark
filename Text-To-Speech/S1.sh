
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  exit 1
fi

IPV4=$1
ACTION="text2speech"
PACKAGE="demo"

pull() {
  
  HUB=onanad
  IMAGE="$HUB/action-python-v3.9:$ACTION"
  SOURCE="speech/__main__.py"
  docker pull  $IMAGE
  wsk action update guest/$PACKAGE/$ACTION --docker $IMAGE $SOURCE --web true
}

prewarm() {

  wsk action invoke $PACKAGE/$ACTION -r --param ipv4 $IPV4
}

echo -e "--->Pull Docker image begin"
pull
echo -e "--->Prewarm Docker image begin"
prewarm

echo -e "--->Experiment begin"
mkdir -p "result/energy/S1/" 
 
for (( i = 1; i <= 10; i++ )); do
  cpu-energy-meter -r >> "result/energy/S1/energy.txt" &
  METER_PID=$!

  wsk action invoke demo/text2speech -r \
    --param ipv4 "$IPV4" \
    --param schema "S1" >>  "result/result.txt"
  kill -SIGINT $METER_PID

  echo -e "$i"

	sleep 2
	
done
    
