
#!/bin/bash

if [ "$#" -ne 1 ]; then

  echo "Usage: $0 <ipv4>"
  echo "ipv4 : ipv4 for swift connection"
  exit 1
fi

IPV4=$1
 
mkdir -p "result/energy/S5/" 
 
for (( i = 1; i <= 10; i++ )); do
    # Launch cpu-energy-meter in background and save her PID
    cpu-energy-meter -r >> "result/energy/S5/energy.txt" &
    METER_PID=$!

    wsk action invoke S5 -r \
      --param ipv4 "$IPV4" \
      --param schema "S5" >>  "result/result.txt"

    kill -SIGINT $METER_PID

    echo -e "$i"
		
	sleep 2
	
done
    
