
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  exit 1
fi

IPV4=$1
TEXT=$2


if [ "$PREWARM" == "1" ]; then

./S3.sh $IPV4 1 0 0 
wsk action update validation  validation/__main__.py
wsk action update S5 --sequence validation,coord,censor

fi


if [ "$RUN" == "1" ]; then
wsk action invoke S5  -r --param ipv4 $IPV4 --param text "1Ko.txt" --param schema "S5"
fi

 
echo -e "--->Experiment begin"
mkdir -p "result/energy/S5/" 

TEXTES=("1Ko.txt" "5Ko.txt" "12Ko.txt" )

for TEXT in "${TEXTES[@]}"; do

  echo -e "$TEXT" 
  for (( i = 1; i <= 2; i++ )); do
    # Launch cpu-energy-meter in background and save her PID
    cpu-energy-meter -r >> "result/energy/S5/$TEXT" &
    METER_PID=$!

    wsk action invoke S5 -r \
      --param ipv4 "$IPV4" \
      --param schema "S5" \
      --param text "$TEXT" >> "result/result.txt"
    kill -SIGINT $METER_PID

    echo -e "$i"

    sleep 6
    
  done

done
    
