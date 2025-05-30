import signal
import os
import subprocess
import time

DURATION = 30
PROCESS  = 4
SCHEMA   = "S1"
IPV4  = "10.245.158.103"
VIDEO = "daenerys.mp4"
RESULT_FILE = "result/result.txt"
ENERGY_DIR = f"result/energy/{SCHEMA}"
ENERGY_FILE = f"{ENERGY_DIR}/{VIDEO}.txt"

processes = []
num_processes = PROCESS
chunk_duration = DURATION // PROCESS

os.makedirs(ENERGY_DIR, exist_ok=True)

for i in range(1, 2):
    
    # cpu-energy-meter in the background.
    energy_process = subprocess.Popen(["cpu-energy-meter", "-r"], stdout=open(ENERGY_FILE, 'a')) 

	# For each expe. we launch each process with part of a video as parameter. 
    for k in range(PROCESS):
        start_time = k * chunk_duration
        
        # print(k)
        

        if k == (num_processes - 1) :
            chunk_duration = chunk_duration + (DURATION%num_processes)

        command = [
        "wsk", "action", "invoke", "S1", "-r", "--blocking",
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
        
    os.kill(energy_process.pid, signal.SIGINT)

    print(i)
    time.sleep(2)

print("All actions have been invoked.")



# wsk action invoke S1 -r --blocking --param ipv4 128.110.96.174 --param start "0"  --param durartion "6"  --param video  "daenerys.mp4"