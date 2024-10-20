
#!/bin/bash
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <ipv4> <VIDEO> <run>"
  echo "ipv4 : ipv4 for swift connection"
  echo "video : video "
  echo "run :  run "
  exit 1
fi
IPV4=$1
VIDEO=$2
RUN=$3
BUILD="pull"

if [ "$BUILD" != "push" ] && [ "$BUILD" != "pull" ]; then
  echo "Invalid build argument. Expected 'push' or 'pull'."
  exit 1   
fi

if [ "$BUILD" == "push" ]; then
  echo "comming son"
else
  docker pull onanad/action-python-v3.9:proc
  wsk action update proc --docker onanad/action-python-v3.9:proc __main__.py -t 125000 -m 1024
fi

# Prewarm the container
wsk action invoke proc --result --param bib moviepy --param file 1Mb.avi --param ipv4 "$IPV4"

# Run the experiment
if [ "$RUN" == "1" ]; then
  LIBRARY=("moviepy" "ffmpeg" "imageio" "opencv")
  RESULT_FILE="result/result.txt"
  ENERGY_DIR="result/energy"

  mkdir -p "$ENERGY_DIR/$VIDEO" 
  
  for LIB in "${LIBRARY[@]}"; do
    echo -e "$LIB"  
    ENERGY_FILE="$ENERGY_DIR/$VIDEO/$LIB$VIDEO.txt"  
      
    for (( i = 1; i <= 10; i++ )); do
      # Launch cpu-energy-meter in background and save her PID
      cpu-energy-meter -r >> $ENERGY_FILE &
      METER_PID=$!
      wsk action invoke proc -r \
        --param bib "$LIB" \
        --param ipv4 "$IPV4" \
        --param file "$VIDEO" >> $RESULT_FILE
      kill -SIGINT $METER_PID
      echo -e "$i"
      sleep 2
    done
      
  done

fi

