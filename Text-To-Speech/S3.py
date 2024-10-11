import sys
import subprocess
import signal
import os

 
def main():
    ipv4 = sys.argv[1]
    speech = [
            "wsk", "action", "invoke", "text2speech", "-r", "--blocking",
            "--param", "ipv4", ipv4, "--param", "schema", "S3"
            ]
    os.makedirs("result/energy/S3", exist_ok=True)
    
    for i in range(2):
        energy_process = subprocess.Popen(["cpu-energy-meter", "-r"], stdout=open("result/energy/S3/energy.txt", 'a'))
        whiskprocess = subprocess.Popen(speech)
        whiskprocess.wait()
        os.kill(energy_process.pid, signal.SIGINT)

main()