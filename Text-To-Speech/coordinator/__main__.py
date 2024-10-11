import requests
from multiprocessing import Process, Manager, Lock


def start(action, args, result, lock):

    apihost = f"http://172.17.0.1:3233/api/v1/web/guest/demo/{action}?blocking=true&result=true"
    
    r = requests.get(apihost, 
                      headers={"Content-Type": "application/json"}, 
                      params=args)

    with lock:
        result.update(r.json())  

     
def main(args):
 
    manager = Manager()
    result = manager.dict()  # Shared dict
    lock = Lock()

    p1 = Process(target=start, args=("S2", args, result, lock))
    p2 = Process(target=start, args=("profanity", args, result, lock))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    return  dict(result)
