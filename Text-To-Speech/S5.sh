
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  exit 1
fi

IPV4=$1

pull() {

  docker pull onanad/action-python-v3.9:censor
  docker pull onanad/action-python-v3.9:text2speech
  docker pull onanad/action-python-v3.9:conversion
  docker pull onanad/action-python-v3.9:profanity

  wsk action update guest/demo/conversion  --docker  onanad/action-python-v3.9:conversion conversion/__main__.py  --web true
  wsk action update guest/demo/text2speech --docker  onanad/action-python-v3.9:text2speech speech/__main__.py     --web true
  wsk action update guest/demo/profanity   --docker  onanad/action-python-v3.9:profanity profanity/__main__.py    --web true
  wsk action update guest/demo/S2  --sequence demo/text2speech,demo/conversion  --web true 
  wsk action update coord coordinator/__main__.py

  wsk action update censor --docker onanad/action-python-v3.9:censor   censor/__main__.py 
  wsk action update validation  validation/__main__.py  

  wsk action update S5 --sequence validation,coord,censor
}

prewarm() {
  wsk action invoke S5  -r --param ipv4 $IPV4
}

echo -e "--->Pull Docker image begin"
pull
echo -e "--->Prewarm Docker image begin"
prewarm

echo -e "--->Experiment begin"
mkdir -p "result/energy/S5/" 

for (( i = 1; i <= 30; i++ )); do
  # Launch cpu-energy-meter in background and save her PID
  cpu-energy-meter -r >> "result/energy/S5/energy.txt" &
  METER_PID=$!

  wsk action invoke S5 -r \
    --param ipv4 "$IPV4" \
    --param schema "S5" >>  "result/result.txt"
  kill -SIGINT $METER_PID

  echo -e "$i"
	sleep 4
	
done
    
