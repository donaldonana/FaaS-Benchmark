import os
import subprocess
import time
import signal

IPV4 = "172.20.10.2"
SCHEMA = "S1"
VIDEO = "daenerys.mp4"
DURATION = 35
PROCESS = 10
RESULT_FILE = "result/result.txt"
ENERGY_DIR = f"result/energy/{SCHEMA}"
ENERGY_FILE = f"{ENERGY_DIR}/{VIDEO}.txt"

os.makedirs(ENERGY_DIR, exist_ok=True)
 
for i in range(1, 2):
    energy_process = subprocess.Popen(["cpu-energy-meter", "-r"], stdout=open(ENERGY_FILE, 'a'))
    try:
        whiskprocess = subprocess.Popen(["python3", 
        f"schema/{SCHEMA}.py", 
        IPV4, str(PROCESS), 
        str(DURATION), 
        SCHEMA, 
        VIDEO, 
        str(i)], 
        stdout=open(RESULT_FILE, 'a'))

    finally:
        whiskprocess.wait()
        os.kill(energy_process.pid, signal.SIGINT)

    print(f"{i}")

    time.sleep(3)

print("All actions have been invoked.")
