#!/bin/bash

IPV4="10.44.193.201"
SCHEMAS=("S1" "S2" "S3" "S4" "S5")
TEXTES=("1Ko.txt" "5Ko.txt" "12Ko.txt")
 

for SCHEMA in "${SCHEMAS[@]}"; do
    echo  -e "$SCHEMA"
    mkdir -p "result/energy/$SCHEMA/" 


    wsk action invoke  "demo/$SCHEMA" -r  --param ipv4   "$IPV4"   # Manually prewarm the container

    for TEXT in "${TEXTES[@]}"; do
        echo "$TEXT" 
        ENERGY_FILE="result/energy/$SCHEMA/$TEXT"
        
        #echo -e "$TEXT" >> perfEnergy.txt
        
        for (( i = 1; i <= 30 ; i++ )); do
        
            cpu-energy-meter -r >> "$ENERGY_FILE" &
            METER_PID=$!

            wsk action invoke  "demo/$SCHEMA" -r \
                --param ipv4   "$IPV4" \
                --param schema "$SCHEMA" \
                --param text   "$TEXT" >> result/result.txt
            
            kill -SIGINT $METER_PID

            # Energy capturing with perf

            # perf stat -o result/perfEnergyS1.txt \
            #     --append -e power/energy-pkg/ -e power/energy-cores/ wsk action invoke demo/text2speech -r \
            #     --param ipv4 "$IPV4" \
            #     --param schema "S1" \
            #     --param text "$TEXT" >> "result/perf.txt"

            echo -e "$i"
            sleep 3
            
        done

    done

    sleep 2


done


 
