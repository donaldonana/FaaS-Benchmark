import sys
import os
import subprocess
import signal


SPEECH_FILE     = "temp/speech.json"
PROFANITY_FILE  = "temp/profanity.json"

def cordinatoor(ipv4):

    processes = []
    speech = [
            "wsk", "action", "invoke", "S2", "-r", "--blocking",
            "--param", "ipv4", ipv4, "--param", "schema", "S1"
            ]
    profanity = [
        "wsk", "action", "invoke", "profanity", "--result",
        "--param", "ipv4", ipv4
    ] 
    processes.append(subprocess.Popen(speech,  stdout=open(SPEECH_FILE, 'w')))
    processes.append(subprocess.Popen(profanity,  stdout=open(PROFANITY_FILE, 'w')))

    for process in processes:
        process.wait()
    
    return {"message" : "Ok"}


def main():
    ipv4 = sys.argv[1]

    speech = [
            "wsk", "action", "invoke", "censor", "-r", "--blocking",
            "--param", "ipv4", ipv4, "-P", SPEECH_FILE, "-P", PROFANITY_FILE
            ]
     
    for i in range(2):

        energy_process = subprocess.Popen(["cpu-energy-meter", "-r"], stdout=open("result/energy/S2/energy.txt", 'a'))
        cordinatoor(ipv4)
        whiskprocess   = subprocess.Popen(speech)
        whiskprocess.wait()
        os.kill(energy_process.pid, signal.SIGINT)
    
    print("----end------")


main()