

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


./S2.sh $IPV4 0 0 0 
wsk action update validation  validation/__main__.py  
wsk action update S4 --sequence validation,demo/text2speech,demo/conversion
 

prewarm() {
  wsk action invoke S4  -r --param ipv4 $IPV4
}

echo -e "--->Pull Docker image begin"
pull
echo -e "--->Prewarm Docker image begin"
prewarm

echo  -e "--->Experiment begin"
mkdir -p "result/energy/S4/" 

TEXTES=("1Ko.txt" "5Ko.txt" "12Ko.txt" )

for TEXT in "${TEXTES[@]}"; do

  echo -e "$TEXT" 
  for (( i = 1; i <= 2; i++ )); do
    # Launch cpu-energy-meter in background and save her PID
    cpu-energy-meter -r >> "result/energy/S4/$TEXT" &
    METER_PID=$!
    wsk action invoke S4 -r \
      --param ipv4 "$IPV4" \
      --param schema "S4" \
      --param text "$TEXT" >> "result/result.txt" 
    kill -SIGINT $METER_PID
    echo -e "$i"
		
	sleep 6
	done

done
    
