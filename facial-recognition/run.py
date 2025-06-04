import signal
import os
import subprocess
import time

DURATION = 30
PROCESS  = 4
SCHEMA   = "S2"
IPV4  = "10.245.158.103"
VIDEO = "daenerys.mp4"
RESULT_FILE = "result/result.txt"
ENERGY_DIR = f"result/energy/{SCHEMA}"
ENERGY_FILE = f"{ENERGY_DIR}/{VIDEO}.txt"

processes = []
num_processes = PROCESS
chunk_duration = DURATION // PROCESS

os.makedirs(ENERGY_DIR, exist_ok=True)



def prewarm(command:list, process:int)-> bool:
    
    print("Prewarm start.")
    
    for k in range(PROCESS):
        start_time = k * chunk_duration
        
        if k == (num_processes - 1) :
            chunk_duration = chunk_duration + (DURATION%num_processes)
            
        process = subprocess.Popen(command, stdout=open(RESULT_FILE, 'a')) # Run each command in the background.
        processes.append(process)

    for process in processes:
        process.wait()
        
    return True 
    

def run(command:list, ntimes:int, process:int) -> bool: 
    ntimes = 2
    
    for i in range(1, ntimes):
        energy_process = subprocess.Popen(["cpu-energy-meter", "-r"], stdout=open(ENERGY_FILE, 'a'))  # cpu-energy-meter the background.
         
        for k in range(PROCESS): # Launch each process with part of a video as parameter.
            start_time = k * chunk_duration
            
            if k == (num_processes - 1) :
                chunk_duration = chunk_duration + (DURATION%num_processes)

            process = subprocess.Popen(command, stdout=open(RESULT_FILE, 'a')) # Run each command in the background.
            processes.append(process)

        for process in processes:
            process.wait()
            
        os.kill(energy_process.pid, signal.SIGINT)

        print(i)
        time.sleep(2)

    return True
        
        
if __name__ == "__main__":
    
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
            
    
    prewarm()
    
    run()
    
    



# wsk action invoke S1 -r --blocking --param ipv4 128.110.96.174 --param start "0"  --param durartion "6"  --param video  "daenerys.mp4"