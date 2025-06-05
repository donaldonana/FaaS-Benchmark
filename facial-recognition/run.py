import signal
import os
import subprocess
import time


IPV4 = "10.44.193.201"


def prewarm(
    nprocess:int,
    duration:int,
    ipv4:str,
    schema:str,
    video:str
    ) -> bool: 
    
    print("prewarm start. \n")
    
    chunk_duration = duration // nprocess
    processes = []
    
    
    for k in range(nprocess):
        start_time = k * chunk_duration
        
        if k == (nprocess - 1) :
            chunk_duration = chunk_duration + (duration%nprocess)
            
        command = [
                "wsk", "action", "invoke", schema, "-r", "--blocking",
                "--param", "ipv4", IPV4,
                "--param", "start", str(start_time),
                "--param", "duration", str(chunk_duration),
                "--param", "schema", schema,
                "--param", "video", video,
                "--param", "chunkdir", f"chunk.{k}",
                "--param", "expe", "0"
            ]
    
        process = subprocess.Popen(command) # Run each command in the background.
        processes.append(process)

    for process in processes:
        process.wait()
        
    return True 
    

def run(
    ntimes:int, 
    nprocess:int,
    duration:int,
    energy_dir:str,
    result_dir:str,
    ipv4:str,
    schema:str,
    video:str
    ) -> bool: 
    """
    Run the benchmark n times.  
    """
    
    energy_file = f"{energy_dir}/{schema}/{video}.txt"
    chunk_duration = DURATION // NPROCESS
    
    print("Runnig Start. \n")
    
    for i in range(1, ntimes):
        energy_process = subprocess.Popen(["cpu-energy-meter", "-r"], stdout=open(energy_file, 'a'))  # cpu-energy-meter in background.
        processes = []
        
        for k in range(nprocess): # Launch each process with part of a video.
            start_time = k * chunk_duration
            
            if k == (nprocess - 1) :
                chunk_duration = chunk_duration + (duration%nprocess)
                
            command = [
                "wsk", "action", "invoke", schema, "-r", "--blocking",
                "--param", "ipv4", ipv4,
                "--param", "start", str(start_time),
                "--param", "duration", str(chunk_duration),
                "--param", "schema", schema,
                "--param", "video", video,
                "--param", "chunkdir", f"chunk.{k}",
                "--param", "expe", str(i)
            ]
            process = subprocess.Popen(command, stdout=open(result_dir, 'a')) # Run each command in the background.
            processes.append(process)

        for process in processes:
            process.wait()
            
        os.kill(energy_process.pid, signal.SIGINT)

        print(i)
        time.sleep(2)

    return True
        
        
if __name__ == "__main__":
    
    DURATION = 30
    NPROCESS = 4
    NTIMES = 2
    VIDEOS = ["daenerys.mp4"]
    SCHEMAS = ["S1"]
    RESULT = "result/result.txt"
    ENERGY = "result/energy/"
    
    os.makedirs(ENERGY, exist_ok=True)
    chunk_duration = DURATION // NPROCESS
    
    for video in VIDEOS:
        print(f"-{video} \n")
        
        for schema in SCHEMAS:
            print(f"--{schema} \n")
            
            prewarm( NPROCESS, DURATION, IPV4, schema, video)
            
            run(NTIMES, NPROCESS, DURATION, ENERGY, RESULT, IPV4, schema, video)
            
    
 
    
    


