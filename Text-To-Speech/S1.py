import sys
import os
import subprocess
import signal


def main():
    ipv4 = sys.argv[1]

    speech = [
            "wsk", "action", "invoke", "censor", "-r", "--blocking",
            "--param", "ipv4", ipv4 
            ]
     
    for i in range(2):

        energy_process = subprocess.Popen(["cpu-energy-meter", "-r"], stdout=open("result/energy/S2/energy.txt", 'a'))
        whiskprocess   = subprocess.Popen(speech)
        whiskprocess.wait()
        os.kill(energy_process.pid, signal.SIGINT)
    
    print("----end------")


main()
