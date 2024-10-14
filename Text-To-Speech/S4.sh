
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  exit 1
fi

IPV4=$1
HUB="onanad"

pull() {
  docker pull $HUB/action-python-v3.9:text2speech
  docker pull $HUB/action-python-v3.9:conversion
  wsk action update guest/demo/conversion  --docker  $HUB/action-python-v3.9:conversion conversion/__main__.py  --web true
  wsk action update guest/demo/text2speech --docker  $HUB/action-python-v3.9:text2speech speech/__main__.py     --web true
  wsk action update validation  validation/__main__.py  
  wsk action update S4 --sequence validation,demo/text2speech,demo/conversion
}

prewarm() {
  wsk action invoke S4  -r --param ipv4 $IPV4
}

echo -e "--->Pull Docker image begin"
pull
echo -e "--->Prewarm Docker image begin"
prewarm

echo  -e "--->Experiment begin"
mkdir -p "result/energy/S4/" 

for (( i = 1; i <= 10; i++ )); do
    # Launch cpu-energy-meter in background and save her PID
    cpu-energy-meter -r >> "result/energy/S4/energy.txt" &
    METER_PID=$!

    wsk action invoke S4 -r \
      --param ipv4 "$IPV4" \
      --param schema "S4" >> "result/result.txt" 

    kill -SIGINT $METER_PID

    echo -e "$i"
		
	sleep 2
	
done
    
