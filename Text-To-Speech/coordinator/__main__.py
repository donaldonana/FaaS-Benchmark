import requests
from multiprocessing import Process, Manager, Lock



def start(action, result, lock):
    
    params = {"ipv4" : "130.190.118.188"}

    r = requests.get(f"http://172.17.0.1:3233/api/v1/web/guest/demo/{action}?blocking=true&result=true", 
                      headers={"Content-Type": "application/json"}, 
                      params=params)

    with lock:
        result.update(r.json())  

    return "ok"

def main(args):

    procs = []
    first  = args.get("first")
    second = args.get("second")

    manager = Manager()
    result = manager.dict()  # Shared dict
    lock = Lock()

    proc = Process(target=start, args=(first,result, lock))
    procs.append(proc)
    proc.start()

    proc = Process(target=start, args=(second,result, lock))
    procs.append(proc)
    proc.start()

    for proc in procs:
        proc.join()

    return  {"args" : str(result)}
