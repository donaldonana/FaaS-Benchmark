import sys
import subprocess


if len(sys.argv) != 7:
    print("Usage: script.py <ipv4> <process> <duration> <schema> <video>")
    print("ipv4 : ipv4 for Swift connection")
    print("process : number of processes to run")
    print("duration : total video duration")
    print("schema : schema")
    print("video : video name")

    sys.exit(1)

ipv4     = sys.argv[1]
process  = int(sys.argv[2])
duration = int(sys.argv[3])
schema   = sys.argv[4]
video    = sys.argv[5]
expe     = sys.argv[6]

 
processes = []
chunk_duration = duration // process
num_processes = process

for i in range(process):   
    start_time = i * chunk_duration

    if i == (num_processes - 1) :
        chunk_duration = chunk_duration + (duration%num_processes)
        print(chunk_duration)

    command = [
        "wsk", "action", "invoke", "S1", "-r", "--blocking",
        "--param", "ipv4", ipv4,
        "--param", "start", str(start_time),
        "--param", "duration", str(chunk_duration),
        "--param", "schema", schema,
        "--param", "video", video,
        "--param", "chunkdir", f"chunk.{i}",
        "--param", "expe", expe
    ]
    # Run each command in the background
    process = subprocess.Popen(command)
    processes.append(process)

for process in processes:
    process.wait()

