import signal
import os
import subprocess
import time

DURATION = 30
PROCESS  = 10
SCHEMA   = "S6"
IPV4  = "172.20.20.78"
VIDEO = "daenerys.mp4"
RESULT_FILE = "result1/result.txt"
ENERGY_DIR = f"result1/energy/{SCHEMA}"
ENERGY_FILE = f"{ENERGY_DIR}/{VIDEO}.txt"

processes = []
num_processes = PROCESS
chunk_duration = DURATION // PROCESS

os.makedirs(ENERGY_DIR, exist_ok=True)

for i in range(1, 3):
    
    # cpu-energy-meter in the background.
    energy_process = subprocess.Popen(["cpu-energy-meter", "-r"], stdout=open(ENERGY_FILE, 'a')) 

	# For each expe. we launch each process with part of a video as parameter. 
    for k in range(PROCESS):
        start_time = k * chunk_duration

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
        
        process = subprocess.Popen(command, stdout=open(RESULT_FILE, 'a')) # Run each command in the background.
        processes.append(process)

    for process in processes:
        process.wait()
        os.kill(energy_process.pid, signal.SIGINT)

    print(i)
    time.sleep(3)

print("All actions have been invoked.")
