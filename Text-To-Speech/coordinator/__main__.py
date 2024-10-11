import requests
from multiprocessing import Process, Manager, Lock


def start(action, result, lock):
    
    params = {"ipv4" : "130.190.118.188"}

    r = requests.get(f"http://172.17.0.1:3233/api/v1/web/guest/demo/{action}?blocking=true&result=true", 
                      headers={"Content-Type": "application/json"}, 
                      params=params)

    with lock:
        result.update(r.json())  

     
def main(args):

    first  = args.get("first")
    second = args.get("second")

    manager = Manager()
    result = manager.dict()  # Shared dict
    lock = Lock()

    p1 = Process(target=start, args=(first,result, lock))
    p2 = Process(target=start, args=(second,result, lock))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    return  dict(result)
