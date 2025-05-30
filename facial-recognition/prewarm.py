import signal
import os
import subprocess
import time

DURATION = 30
PROCESS  = 10
SCHEMA   = "S2"
IPV4  = "10.245.158.103"
VIDEO = "daenerys.mp4"

processes = []
num_processes = PROCESS
chunk_duration = DURATION // PROCESS

os.makedirs(ENERGY_DIR, exist_ok=True)

for i in range(1, 2):
     
    for k in range(PROCESS):
        start_time = k * chunk_duration

        if k == (num_processes - 1) :
            chunk_duration = chunk_duration + (DURATION%num_processes)

        command = [
        "wsk", "action", "invoke", SCHEMA, "-r", "--blocking",
        "--param", "ipv4", IPV4,
        "--param", "start", str(start_time),
        "--param", "duration", str(chunk_duration),
        "--param", "schema", SCHEMA,
        "--param", "video", VIDEO,
        "--param", "chunkdir", f"chunk.{k}",
        "--param", "expe", str(i)
    	]
        
        process = subprocess.Popen(command) # Run each command in the background.
        processes.append(process)

    for process in processes:
        process.wait()
        
    print(i)
    time.sleep(2)

print("All actions have been invoked.")



# wsk action invoke S1 -r --blocking --param ipv4 128.110.96.174 --param start "0"  --param durartion "6"  --param video  "daenerys.mp4"